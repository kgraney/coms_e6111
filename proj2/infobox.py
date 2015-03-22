import abc
import itertools
import logging
import math
import textwrap

import freebase

logger = logging.getLogger(__name__)

class Infobox(object):
    def __init__(self):
        self.entities = []

    def Print(self):
        properties = []
        entity_names = []
        for entity in self.entities:
            entity_names.append(entity.__class__.__name__)
            for p in entity.GetProperties():
                properties.append(p)

        label_col_width = max(p.GetLabelWidth() for p in properties)
        data_col_width = 123 - label_col_width
        print '+ ' + '-'*label_col_width + '---' + '-'*data_col_width + ' +'
        print entity_names

        divider = '+ ' + '-'*label_col_width + ' + ' + '-'*data_col_width + ' +'
        for p in properties:
            rows = itertools.izip_longest(p.GetLabelRows(label_col_width),
                                          p.GetContentRows(data_col_width),
                                          fillvalue='')
            print divider
            for l,c in rows:
                line = '| %s | %s |' % (l.ljust(label_col_width),
                                        c.ljust(data_col_width))
                print line
        print divider

    @classmethod
    def ConstructFromTrie(cls, root_trie):
        logger.info('Constructing Infobox')
        obj = cls()
        classes = set()
        for entity_id, entity_class in ENTITY_MAP.items():
            entity = root_trie.MatchEntityId(entity_id)
            if entity is not None and entity_class not in classes:
                obj.entities.append(entity_class(root_trie))
                classes.add(entity_class)
        return obj

class InfoboxProperty(object):
    def __init__(self, name):
        self.name = name

    def GetLabelWidth(self):
        return len(self.name)

    def GetLabelRows(self, width):
        return [self.name]

class InfoboxListProperty(InfoboxProperty):
    def __init__(self, name):
        super(InfoboxListProperty, self).__init__(name)
        self.lst = []

    def AddTextToList(self, text):
        self.lst.append(text)

    def GetContentRows(self, width):
        rows = []
        if (len(self.lst) > 1):
            kwargs = {'initial_indent':'* ', 'subsequent_indent':'  '}
        else:
            kwargs = {}
        for item in self.lst:
            rows.extend(textwrap.wrap(item, width, **kwargs))
        return rows

class InfoboxTableProperty(InfoboxProperty):
    def __init__(self, name):
        super(InfoboxTableProperty, self).__init__(name)
        self.table = {}

    def AddColumnValue(self, row, column_name, value):
        self.table.setdefault(row, {})[column_name] = value

    def GetContentRows(self, width):
        column_titles = set(
                item for sublist in (x.keys() for x in self.table.values())
                for item in sublist)
        cols = {}
        for column in column_titles:
            cols[column] = []
            for row in self.table.values():
                cols[column].append(row.get(column, ''))

        column_widths = {}
        for col_name in cols:
            column_widths[col_name] = max(len(x)
                                          for x in cols[col_name] + [col_name])

        preferred_width = sum(column_widths.values()) + 3*(len(column_widths) - 1)
        if preferred_width > width:
            adjustment = (preferred_width - width) / len(cols)
            for col_name in cols:
                column_widths[col_name] -= adjustment

        for col_name in cols:
            cols[col_name] = [
                    x[:column_widths[col_name]].ljust(column_widths[col_name])
                    for x in cols[col_name]]

        # This is safe if cols isn't modified during these operations.
        rows = [' | '.join(x.ljust(column_widths[x]) for x in cols.keys())]
        rows.append('-'*width)
        rows.extend(' | '.join(x) for x in zip(*cols.values()))
        return rows

class InfoboxEntity(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, entity_trie):
        self.properties = {}
        self.ParseTrie(entity_trie)

    def ParseTrie(self, root):
        for prop_id, prop_name in self.GetInterestingProperties().iteritems():
            entity = root.MatchEntityId(prop_id)
            if entity is None:
                continue
            for row, c in enumerate(entity.value):
                if 'property' in c:
                    self.ProcessProperty(row, prop_name, c)
                else:
                    if 'value' in c:
                        self.ProcessText(prop_name, c['value'])
                    else:
                        self.ProcessText(prop_name, c['text'])

    def ProcessProperty(self, row, tag, data):
        trie = freebase.EntityNode.ConstructTrie(
                dict((x[0], x[1]['values']) for x in data['property'].items()))
        for prop_id, column_name in self.GetTableColumns().items():
            entity = trie.MatchEntityId(prop_id)
            if entity is None:
                continue
            for c in entity.value:
                if 'value' in c:
                    self.properties.setdefault(tag,
                            InfoboxTableProperty(tag)).AddColumnValue(row, column_name, c['value'])
                else:
                    self.properties.setdefault(tag,
                            InfoboxTableProperty(tag)).AddColumnValue(row, column_name, c['text'])

    def ProcessText(self, tag, text):
        self.properties.setdefault(tag,
                InfoboxListProperty(tag)).AddTextToList(text)

    def GetProperties(self):
        return self.properties.values()

    #@abc.abstractmethod
    def GetInterestingProperties(self):
        return {}

    def GetTableColumns(self):
        return {}

class Person(InfoboxEntity):
    PROPERTIES = {
            '/type/object/name': 'Name',
            '/people/person/place_of_birth': 'Place of Birth',
            '/people/person/date_of_birth': 'Birthday',
            '/people/person/spouse_s': 'Spouses',
            '/people/person/sibling_s': 'Siblings',
            '/common/topic/description': 'Description',
            '/people/deceased_person/cause_of_death': 'Cause of Death',
            '/people/deceased_person/date_of_death': 'Date of Death',
            '/people/deceased_person/place_of_death': 'Place of Death',
            }

    TABLE_COLUMNS = {
            '/people/sibling_relationship/sibling': 'Sibling',
            '/people/marriage/spouse': 'Spouse',
            '/people/marriage/location_of_ceremony': 'Location',
            '/people/marriage/from': 'From',
            '/people/marriage/to': 'To',
            }

    def GetInterestingProperties(self):
        return self.PROPERTIES

    def GetTableColumns(self):
        return self.TABLE_COLUMNS

class Author(InfoboxEntity):
    PROPERTIES = {
            '/book/author/works_written': 'Books',
            '/book/book_subject/works': 'Book about',
            '/influence/influence_node/influenced': 'Influenced',
            '/influence/influence_node/influenced_by': 'Influenced by',
            }

    def GetInterestingProperties(self):
        return self.PROPERTIES

class Actor(InfoboxEntity):
    PROPERTIES = {
            '/film/actor/film': 'Films',
            }

    TABLE_COLUMNS = {
            '/film/performance/character': 'Character',
            '/film/performance/film': 'Film name',
            }

    def GetInterestingProperties(self):
        return self.PROPERTIES

    def GetTableColumns(self):
        return self.TABLE_COLUMNS


class BusinessPerson(InfoboxEntity):
    PROPERTIES = {
            '/organization/organization_founder/organizations_founded': 'Founded',
            '/business/board_member/organization_board_memberships': 'Board member',
            '/business/board_member/leader_of': 'Leadership',
            }

    TABLE_COLUMNS = {
            '/organization/organization_board_membership/from': 'From',
            '/organization/organization_board_membership/to': 'To',
            '/organization/organization_board_membership/organization': 'Organization',
            '/organization/organization_board_membership/role': 'Role',
            '/organization/organization_board_membership/title': 'Title',
            '/organization/leadership/from': 'From',
            '/organization/leadership/to': 'To',
            '/organization/leadership/organization': 'Organization',
            '/organization/leadership/role': 'Role',
            '/organization/leadership/title': 'Title',
            }

    def GetInterestingProperties(self):
        return self.PROPERTIES

    def GetTableColumns(self):
        return self.TABLE_COLUMNS

class League(InfoboxEntity):
    PROPERTIES = {
            '/type/object/name': 'Name',
            '/common/topic/description': 'Description',
            '/sports/sports_league/sport': 'Sport',
            '/organization/organization/slogan': 'Slogan',
            '/common/topic/official_website': 'Official website',
            '/sports/sports_league/championship': 'Championship',
            '/sports/sports_league/teams': 'Teams',
            }

    TABLE_COLUMNS = {
            '/sports/sports_league_participation/team': 'Team Name',
            }

    def GetInterestingProperties(self):
        return self.PROPERTIES

    def GetTableColumns(self):
        return self.TABLE_COLUMNS

class SportsTeam(InfoboxEntity):
    PROPERTIES = {
            '/type/object/name': 'Name',
            '/common/topic/description': 'Description',
            '/sports/sports_team/sport': 'Sport',
            '/sports/sports_team/roster': 'Roster',
            '/sports/sports_team/championships': 'Championships',
            '/sports/sports_team/arena_stadium': 'Arena',
            '/sports/sports_team/founded': 'Founded',
            '/sports/sports_team/league': 'Leagues',
            '/sports/sports_team/location': 'Locations',
            '/sports/sports_team/coaches': 'Coaches',
            '/sports/sports_team/roster': 'Players',
            }

    TABLE_COLUMNS = {
            '/sports/sports_team_coach_tenure/coach': 'Name',
            '/sports/sports_team_coach_tenure/to': 'To',
            '/sports/sports_team_coach_tenure/from': 'From',
            '/sports/sports_team_coach_tenure/position': 'Position',
            '/sports/sports_team_roster/from': 'From',
            '/sports/sports_team_roster/to': 'To',
            '/sports/sports_team_roster/player': 'Name',
            '/sports/sports_team_roster/position': 'Position',
            '/sports/sports_team_roster/number': 'Number',
            '/sports/sports_league_participation/league': 'League',
            }

    def GetInterestingProperties(self):
        return self.PROPERTIES

    def GetTableColumns(self):
        return self.TABLE_COLUMNS

ENTITY_MAP = {
        '/people/person': Person,
        '/book/author': Author,
        '/film/actor': Actor,
        '/tv/tv_actor': Actor,
        '/organization/organization_founder': BusinessPerson,
        '/business/board_member': BusinessPerson,
        '/sports/sports_league': League,
        '/sports/sports_team': SportsTeam,
        '/sports/professional_sports_team': SportsTeam
        }


