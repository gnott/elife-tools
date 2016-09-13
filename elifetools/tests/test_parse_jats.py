import unittest
import os
import json
from ddt import ddt, data, unpack
from bs4 import BeautifulSoup

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import parseJATS as parser
import rawJATS as raw_parser
from utils import date_struct

from file_utils import sample_xml, json_expected_folder, json_expected_file




@ddt
class TestParseJats(unittest.TestCase):

    def setUp(self):
        pass

    def soup(self, filename):
        # return soup
        return parser.parse_document(sample_xml(filename))

    def json_expected(self, filename, function_name):
        json_expected = None
        json_file = json_expected_file(filename, function_name)
        try:
            with open(json_file, 'rb') as json_file_fp:
                json_expected = json.loads(json_file_fp.read())
        except IOError:
            # file may not exist or the value is None for this article
            pass
        return json_expected

    @data("elife-kitchen-sink.xml")
    def test_parse_document(self, filename):
        soup = parser.parse_document(sample_xml(filename))
        self.assertTrue(isinstance(soup, BeautifulSoup))


    """
    Unit test small or special cases
    """
    @unpack
    @data(("", ""),
        ("<email>test@example.org</email>", "test@example.org"))
    def test_get_email(self, text, expected):
        self.assertEqual(expected, parser.get_email(text))

    @unpack
    @data(("elife-kitchen-sink.xml", "pub", ('28', '02', '2014')))
    def test_ymd(self, filename, test_date_type, expected):
        soup = self.soup(filename)
        date_tag = raw_parser.pub_date(soup, date_type=test_date_type)
        self.assertEqual(expected, parser.ymd(date_tag))

    @unpack
    @data(("elife-kitchen-sink.xml", "received", date_struct(2012, 6, 22)),
        ("elife-kitchen-sink.xml", None, None),
        ("elife-kitchen-sink.xml", "not_a_date_type", None))
    def test_history_date(self, filename, date_type, expected):
        self.assertEqual(expected, parser.history_date(self.soup(filename), date_type))


    """
    Functions that require more than one argument to test against json output
    """

    @data("elife-kitchen-sink.xml")
    def test_journal_issn(self, filename):
        self.assertEqual(self.json_expected(filename, "journal_issn"),
                         parser.journal_issn(self.soup(filename), "electronic"))

    @data("elife-kitchen-sink.xml", "elife00240.xml")
    def test_author_contributions(self, filename):
        self.assertEqual(self.json_expected(filename, "author_contributions"),
                         parser.author_contributions(self.soup(filename), "con"))

    @data("elife-kitchen-sink.xml", "elife00190.xml")
    def test_competing_interests(self, filename):
        self.assertEqual(self.json_expected(filename, "competing_interests"),
                         parser.competing_interests(self.soup(filename), "conflict"))

    @data("elife-kitchen-sink.xml")
    def test_full_author_notes(self, filename):
        self.assertEqual(self.json_expected(filename, "full_author_notes"),
                         parser.full_author_notes(self.soup(filename), None))

    """
    Functions that only need soup to test them against json output
    """

    @data("elife-kitchen-sink.xml", "elife07586.xml")
    def test_abstract(self, filename):
        self.assertEqual(self.json_expected(filename, "abstract"),
                         parser.abstract(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00013.xml", "elife_poa_e06828.xml")
    def test_abstracts(self, filename):
        self.assertEqual(self.json_expected(filename, "abstracts"),
                         parser.abstracts(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_accepted_date_date(self, filename):
        self.assertEqual(self.json_expected(filename, "accepted_date_date"),
                         parser.accepted_date_date(self.soup(filename)))


    @data("elife-kitchen-sink.xml")
    def test_accepted_date_day(self, filename):
        self.assertEqual(self.json_expected(filename, "accepted_date_day"),
                         parser.accepted_date_day(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_accepted_date_month(self, filename):
        self.assertEqual(self.json_expected(filename, "accepted_date_month"),
                         parser.accepted_date_month(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_accepted_date_timestamp(self, filename):
        self.assertEqual(self.json_expected(filename, "accepted_date_timestamp"),
                         parser.accepted_date_timestamp(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_accepted_date_year(self, filename):
        self.assertEqual(self.json_expected(filename, "accepted_date_year"),
                         parser.accepted_date_year(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_ack(self, filename):
        self.assertEqual(self.json_expected(filename, "ack"),
                         parser.ack(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_acknowledgements(self, filename):
        self.assertEqual(self.json_expected(filename, "acknowledgements"),
                         parser.acknowledgements(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_article_type(self, filename):
        self.assertEqual(self.json_expected(filename, "article_type"),
                         parser.article_type(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00013.xml", "elife00240.xml")
    def test_author_notes(self, filename):
        self.assertEqual(self.json_expected(filename, "author_notes"),
                         parser.author_notes(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00013.xml", "elife_poa_e06828.xml",
          "elife02935.xml", "elife00270.xml", "elife00351.xml")
    def test_authors(self, filename):
        self.assertEqual(self.json_expected(filename, "authors"),
                         parser.authors(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_authors_non_byline(self, filename):
        self.assertEqual(self.json_expected(filename, "authors_non_byline"),
                         parser.authors_non_byline(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife-09215-v1.xml", "elife00013.xml")
    def test_award_groups(self, filename):
        self.assertEqual(self.json_expected(filename, "award_groups"),
                         parser.award_groups(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_category(self, filename):
        self.assertEqual(self.json_expected(filename, "category"),
                         parser.category(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_collection_year(self, filename):
        self.assertEqual(self.json_expected(filename, "collection_year"),
                         parser.collection_year(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_component_doi(self, filename):
        self.assertEqual(self.json_expected(filename, "component_doi"),
                         parser.component_doi(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife02304.xml", "elife05502.xml", "elife04490.xml",
          "elife-14093-v1.xml")
    def test_components(self, filename):
        self.assertEqual(self.json_expected(filename, "components"),
                         parser.components(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_conflict(self, filename):
        self.assertEqual(self.json_expected(filename, "conflict"),
                         parser.conflict(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_contributors(self, filename):
        self.assertEqual(self.json_expected(filename, "contributors"),
                         parser.contributors(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_copyright_holder(self, filename):
        self.assertEqual(self.json_expected(filename, "copyright_holder"),
                         parser.copyright_holder(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_copyright_statement(self, filename):
        self.assertEqual(self.json_expected(filename, "copyright_statement"),
                         parser.copyright_statement(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_copyright_year(self, filename):
        self.assertEqual(self.json_expected(filename, "copyright_year"),
                         parser.copyright_year(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_correspondence(self, filename):
        self.assertEqual(self.json_expected(filename, "correspondence"),
                         parser.correspondence(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife07586.xml", "elife_poa_e06828.xml")
    def test_digest(self, filename):
        self.assertEqual(self.json_expected(filename, "digest"),
                         parser.digest(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_display_channel(self, filename):
        self.assertEqual(self.json_expected(filename, "display_channel"),
                         parser.display_channel(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_doi(self, filename):
        self.assertEqual(self.json_expected(filename, "doi"),
                         parser.doi(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_elocation_id(self, filename):
        self.assertEqual(self.json_expected(filename, "elocation_id"),
                         parser.elocation_id(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife07586.xml", "elife_poa_e06828.xml", "elife00013.xml")
    def test_full_abstract(self, filename):
        self.assertEqual(self.json_expected(filename, "full_abstract"),
                         parser.full_abstract(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_full_affiliation(self, filename):
        self.assertEqual(self.json_expected(filename, "full_affiliation"),
                         parser.full_affiliation(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_full_award_group_funding_source(self, filename):
        self.assertEqual(self.json_expected(filename, "full_award_group_funding_source"),
                         parser.full_award_group_funding_source(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_full_award_groups(self, filename):
        self.assertEqual(self.json_expected(filename, "full_award_groups"),
                         parser.full_award_groups(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_full_correspondence(self, filename):
        self.assertEqual(self.json_expected(filename, "full_correspondence"),
                         parser.full_correspondence(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife07586.xml", "elife_poa_e06828.xml")
    def test_full_digest(self, filename):
        self.assertEqual(self.json_expected(filename, "full_digest"),
                         parser.full_digest(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_full_keyword_groups(self, filename):
        self.assertEqual(self.json_expected(filename, "full_keyword_groups"),
                         parser.full_keyword_groups(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_full_license(self, filename):
        self.assertEqual(self.json_expected(filename, "full_license"),
                         parser.full_license(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_full_subject_area(self, filename):
        self.assertEqual(self.json_expected(filename, "full_subject_area"),
                         parser.full_subject_area(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_full_title(self, filename):
        self.assertEqual(self.json_expected(filename, "full_title"),
                         parser.full_title(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_funding_statement(self, filename):
        self.assertEqual(self.json_expected(filename, "funding_statement"),
                         parser.funding_statement(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00013.xml", "elife00240.xml",
          "elife04953.xml", "elife00133.xml")
    def test_graphics(self, filename):
        self.assertEqual(self.json_expected(filename, "graphics"),
                         parser.graphics(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_impact_statement(self, filename):
        self.assertEqual(self.json_expected(filename, "impact_statement"),
                         parser.impact_statement(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00240.xml")
    def test_inline_graphics(self, filename):
        self.assertEqual(self.json_expected(filename, "inline_graphics"),
                         parser.inline_graphics(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_is_poa(self, filename):
        self.assertEqual(self.json_expected(filename, "is_poa"),
                         parser.is_poa(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_journal_id(self, filename):
        self.assertEqual(self.json_expected(filename, "journal_id"),
                         parser.journal_id(self.soup(filename)))



    @data("elife-kitchen-sink.xml")
    def test_journal_title(self, filename):
        self.assertEqual(self.json_expected(filename, "journal_title"),
                         parser.journal_title(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife07586.xml")
    def test_keywords(self, filename):
        self.assertEqual(self.json_expected(filename, "keywords"),
                         parser.keywords(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_license(self, filename):
        self.assertEqual(self.json_expected(filename, "license"),
                         parser.license(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_license_url(self, filename):
        self.assertEqual(self.json_expected(filename, "license_url"),
                         parser.license_url(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife02304.xml", "elife00007.xml", "elife04953.xml",
          "elife00005.xml", "elife05031.xml", "elife04493.xml", "elife06726.xml")
    def test_media(self, filename):
        self.assertEqual(self.json_expected(filename, "media"),
                         parser.media(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_timestamp(self, filename):
        self.assertEqual(self.json_expected(filename, "pub_date_timestamp"),
                         parser.pub_date_timestamp(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_date(self, filename):
        self.assertEqual(self.json_expected(filename, "pub_date_date"),
                         parser.pub_date_date(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_day(self, filename):
        self.assertEqual(self.json_expected(filename, "pub_date_day"),
                         parser.pub_date_day(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_month(self, filename):
        self.assertEqual(self.json_expected(filename, "pub_date_month"),
                         parser.pub_date_month(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_pub_date_year(self, filename):
        self.assertEqual(self.json_expected(filename, "pub_date_year"),
                         parser.pub_date_year(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_publisher(self, filename):
        self.assertEqual(self.json_expected(filename, "publisher"),
                         parser.publisher(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_publisher_id(self, filename):
        self.assertEqual(self.json_expected(filename, "publisher_id"),
                         parser.publisher_id(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_received_date_date(self, filename):
        self.assertEqual(self.json_expected(filename, "received_date_date"),
                         parser.received_date_date(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_received_date_day(self, filename):
        self.assertEqual(self.json_expected(filename, "received_date_day"),
                         parser.received_date_day(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_received_date_month(self, filename):
        self.assertEqual(self.json_expected(filename, "received_date_month"),
                         parser.received_date_month(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_received_date_timestamp(self, filename):
        self.assertEqual(self.json_expected(filename, "received_date_timestamp"),
                         parser.received_date_timestamp(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_received_date_year(self, filename):
        self.assertEqual(self.json_expected(filename, "received_date_year"),
                         parser.received_date_year(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_references(self, filename):
        # Alias of refs
        self.assertEqual(self.json_expected(filename, "refs"),
                         parser.references(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife00013.xml", "elife02935.xml", "elife00051.xml",
          "elife_poa_e06828.xml")
    def test_refs(self, filename):
        self.assertEqual(self.json_expected(filename, "refs"),
                         parser.refs(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_related_article(self, filename):
        self.assertEqual(self.json_expected(filename, "related_article"),
                         parser.related_article(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_related_object_ids(self, filename):
        self.assertEqual(self.json_expected(filename, "related_object_ids"),
                         parser.related_object_ids(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife07586.xml")
    def test_research_organism(self, filename):
        self.assertEqual(self.json_expected(filename, "research_organism"),
                         parser.research_organism(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_self_uri(self, filename):
        self.assertEqual(self.json_expected(filename, "self_uri"),
                         parser.self_uri(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_subject_area(self, filename):
        self.assertEqual(self.json_expected(filename, "subject_area"),
                         parser.subject_area(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml", "elife02304.xml")
    def test_supplementary_material(self, filename):
        self.assertEqual(self.json_expected(filename, "supplementary_material"),
                         parser.supplementary_material(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_title(self, filename):
        self.assertEqual(self.json_expected(filename, "title"),
                         parser.title(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_title_short(self, filename):
        self.assertEqual(self.json_expected(filename, "title_short"),
                         parser.title_short(self.soup(filename)))

    @data("elife-kitchen-sink.xml")
    def test_title_slug(self, filename):
        self.assertEqual(self.json_expected(filename, "title_slug"),
                         parser.title_slug(self.soup(filename)))

    @data("elife-kitchen-sink.xml", "elife_poa_e06828.xml")
    def test_volume(self, filename):
        self.assertEqual(self.json_expected(filename, "volume"),
                         parser.volume(self.soup(filename)))






if __name__ == '__main__':
    unittest.main()