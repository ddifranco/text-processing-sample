#! /usr/bin/python3

import re
from collections import OrderedDict
import pdb

class Extractor():

    replacements = {}
    replacements["V"] = ["visual acuity:", "visual acuity", "va:", "va", "vacc:", "vacc"]
    replacements["C"] = ["cc:", "cc", "corrected:", "corrected"]
    replacements["P"] = ["ph:", "ph", "pinhole:", "pinhole"]
    replacements["R"] = ["re:", "re", "od:", "od"]
    replacements["L"] = ["le:", "le", "os:", "os"]
    replacements["p"] = ["+"]         #replacements +/- while not strictly necessary allow for simpler regexs and reduce risk of error
    replacements["m"] = ["-"]
    replacements["/9"] = ["/"]        #prepend a 9 to prevent empty subgroups - note that this will have to be reversed 
    replacements["20/9888"] = ["ni"]  #ni coded internally as 888

    measurement = "R20\/([0-9]+)[mp]?[0-9]?L20\/([0-9]+)[mp]?[0-9]?"
    right_only = "R20\/([0-9]+)[mp]?[0-9]?"
    m_patterns = OrderedDict()  #Need to use an ordered dict to control testing order. This in turn ensures both tests are identified when present
    m_patterns["both"] = re.compile(f"VC{measurement}P{measurement}")
    m_patterns["both_noleft"] = re.compile(f"VC{measurement}P{right_only}")
    m_patterns["cc_v1"] = re.compile(f"V{measurement}")
    m_patterns["cc_v2"] = re.compile(f"VC{measurement}")
    m_patterns["ph"] = re.compile(f"VP{measurement}")

    def extract(self, original):
        """
        Extracts all possible measurements from a raw document
        """

        final = {"cc_le": None, "cc_re" : None, "ph_le" : None, "ph_re" : None}

        normalized = self.normalize(original)
        pattern, result = self.attempt_match(normalized)

        if pattern == "both": 
            final["cc_re"] = result.group(1)[1:]    #slice off 0th position, which contains a 9
            final["cc_le"] = result.group(2)[1:]
            final["ph_re"] = result.group(3)[1:]
            final["ph_le"] = result.group(4)[1:]

        if pattern == "both_noleft": 
            final["cc_re"] = result.group(1)[1:]
            final["cc_le"] = result.group(2)[1:]
            final["ph_re"] = result.group(3)[1:]

        if pattern in ["cc_v1", "cc_v2"]: 
            final["cc_re"] = result.group(1)[1:]
            final["cc_le"] = result.group(2)[1:]

        if pattern == "ph":
            final["ph_re"] = result.group(1)[1:]
            final["ph_le"] = result.grpup(2)[1:]

        for k, v in final.items():
            if v == '':
                final[k] = None
            if v not in ['', None]:
                final[k] = int(v)

        return final["cc_re"], final["cc_le"], final["ph_re"], final["ph_le"]

    def normalize(self, raw):
        """
        Makes some replacements to ensure conformity with a limited set of regexes
        """

        normalized = raw.lower()

        for standard, alternatives in self.replacements.items():
            for alternative in alternatives:
                normalized = normalized.replace(alternative, standard)

        normalized = normalized.replace(" ", "")

        return normalized


    def attempt_match(self, processed):
        """
        Tries to match patterns against preprocessed document;
        Returns the first match
        """

        for k, v in self.m_patterns.items(): 
            match = re.match(v, processed) 
            if match is not None:
                return k, match


        return "none", None
