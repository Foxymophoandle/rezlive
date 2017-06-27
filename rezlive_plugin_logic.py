#!/usr/bin/env python
from xml.etree.ElementTree import Element, SubElement

from pluginframework.exceptions import EpycsStandardException
from pluginframework.plugin_logic import PluginLogic
from pluginframework.plugin_structs import PluginDoc, FeatureImplLevel
from pluginframework.shiva import lookup_hotel, lookup_room
from pluginframework.xmlrequester import XmlRequester
from rezlive.rezlive_utils import remove_namespaces

__author__ = 'davide'
__date__ = ' 27 June 2017'

class BaseRequester(XmlRequester):

    def __init__(self, plogic):
        super(BaseRequester, self).__init__(headers={'method': 'POST',
                                                     'Content-type': 'text/xml; charset=utf-8',
                                                     'Content-Length': ''})
        self.plogic = plogic
        self.prefix = plogic.contract_id_shadow_prefix
        self.logger = self.plogic.avail_log
        self.result = None

    def get_url(self, input_dict):
        """
        Url is composed by different parts to be glued together in
        a correct url format
        """
        if type(input_dict) is dict:
            url = input_dict['_additional']['account']['url']
        else:
            url = input_dict.configuration['url']
        # # We take each part, remove eventual trailing slashes and join them together with slashes again
        # url = '/'.join(map(lambda x: str(x).rstrip('/'), [url, self.CUSTOM_URL_PART, URL_SUFFIX]))
        return url

    def get_request_elem(self, input_dict):
        """
        The only method to implement will be the build_req_elem
        """
        root_elem = Element(_NS_SOAP + 'Envelope')
        root_elem.append(self._build_header_elem(input_dict))
        body_elem = SubElement(root_elem, _NS_SOAP + 'Body')
        body_elem.append(self.build_request_elem(input_dict))
        return root_elem

    def _build_header_elem(self, input_dict):
        """
        Setting credentials from account here
        """
        header_elem = Element(_NS_SOAP + 'Header')
        return header_elem

    def build_request_elem(self, input_dict):
        raise NotImplementedError()

    def handle_response(self, input_dict, response_elem):
        """
        We perform common tasks and handle errors here.
        the method to be implemented by each requester is parse_response
        """
        remove_namespaces(response_elem)
        error_text = self.may_get_error_text(response_elem)
        self.handle_errors(error_text, input_dict)
        result = self.parse_response(input_dict, response_elem)
        self.result = result
        return result

    def may_get_error_text(self, response_elem):
        """
        We return error text if any
        """
        error_elems = response_elem.findall('.//Error')
        if len(error_elems) > 0:
            return error_elems[0].text
        return None

    def handle_errors(self, error_text, input_dict):
        """
        We log error and raise a standard exception
        """
        if error_text:
            self.logger.warning('%s FAILED: %s' % (self.__class__.__name__, error_text))
            raise EpycsStandardException(error_text)

    def parse_response(self, input_dict, response_elem):
        raise NotImplementedError()

    def translate_hotel_info(self, supplier_hotel_code):
        """Wrapper of lookup hotel catching exception and returning None
        """
        internal_hotel_info = None
        try:
            internal_hotel_info = lookup_hotel(self.plogic.shiva, supplier_hotel_code)
        except:
            pass
        return internal_hotel_info

    def translate_room_info(self, supplier_ctype):
        """Wrapper of lookup ctype catching exception and returning None
        """
        internal_ctype_info = None
        try:
            internal_ctype_info = lookup_room(self.plogic.shiva, supplier_ctype)
        except:
            pass
        return internal_ctype_info


# noinspection PyTypeChecker
class RezlivePluginLogic(PluginLogic):

    def __init__(self, name, contract_id_prefix, shiva, avail_log, booking_log):
        super(RezlivePluginLogic, self).__init__(name, contract_id_prefix, shiva, avail_log, booking_log)

    def get_account_keys(self):
        return ['url', 'markup', 'username', 'password', 'default_nationality']

    def are_avail_precondition_satisfied(self, query):
        """
        """
        return True
    #
    # def get_avail_requesters(self, input_dict):
    #     return [AvailabilityRequester(self)]
    #
    # def get_avail_deadline_requesters(self, input_dict):
    #     return [AvailDeadlineRequester(self)]
    #
    # def get_booking_requesters(self, input_dict):
    #     return [
    #         AvailabilityRequester(self),
    #         ReservationRequestRequester(self, prebook=True),
    #         ReservationRequestRequester(self),
    #     ]
    #
    # def get_details_booking_requesters(self, input_dict):
    #     return [ReadBookingRequester(self)]
    #
    # def get_cancel_booking_requesters(self, input_dict):
    #     return [
    #         CancelBookingRequester(self, precancel=True),
    #         CancelBookingRequester(self),
    #     ]

    def import_hotel_details(self, account, hotel_code, support):
        return None

    def import_supplier_data(self, account):
        return None

    @staticmethod
    def get_documentation():
        plugin_doc = PluginDoc()
        # plugin_doc.encoding = 'utf-8'
        # plugin_doc.on_request_availability = FeatureImplLevel.YES
        # plugin_doc.real_time_searches = FeatureImplLevel.YES
        # plugin_doc.cot = FeatureImplLevel.YES
        # plugin_doc.extra_beds = FeatureImplLevel.YES
        # plugin_doc.accurate_deadline = FeatureImplLevel.YES
        # plugin_doc.structured_deadline = FeatureImplLevel.YES
        # plugin_doc.booking_synchronous = FeatureImplLevel.YES
        # plugin_doc.deadline_shown_after_selection = FeatureImplLevel.YES
        # plugin_doc.accurate_price_breakdown = FeatureImplLevel.NO
        # plugin_doc.accurate_meals = FeatureImplLevel.NO
        # plugin_doc.accurate_ctype = FeatureImplLevel.YES
        # plugin_doc.flexible_room_mapping = FeatureImplLevel.YES
        # plugin_doc.accurate_double_twin_mapping = FeatureImplLevel.NO
        # plugin_doc.accurate_single_tsu_mapping = FeatureImplLevel.NO
        # plugin_doc.multi_room_allowed = FeatureImplLevel.YES
        # plugin_doc.remarks_to_supplier = FeatureImplLevel.NO
        # plugin_doc.remarks_from_supplier = FeatureImplLevel.YES
        # plugin_doc.booking_deletion = FeatureImplLevel.YES
        # plugin_doc.change_operation = FeatureImplLevel.NO
        # plugin_doc.change_allows_add = FeatureImplLevel.NO
        # plugin_doc.search_by_hotel_id = FeatureImplLevel.YES
        # plugin_doc.search_by_multi_hotel_id = FeatureImplLevel.YES
        # plugin_doc.search_by_id_requires_city = FeatureImplLevel.NO
        # plugin_doc.xml_compression = FeatureImplLevel.YES
        # plugin_doc.pax_nationality_iso2 = FeatureImplLevel.YES
        # plugin_doc.pax_nationality_iso3 = FeatureImplLevel.NO
        # plugin_doc.pax_nationality_mapping = FeatureImplLevel.NO
        # plugin_doc.pax_nationality_multi_account = FeatureImplLevel.NO
        return plugin_doc
