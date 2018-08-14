import re
import json

import pkg_resources
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String
from xblock.fragment import Fragment

import requests

BASE_URL = "http://ec2-54-156-197-224.compute-1.amazonaws.com"
PORT     = "3050"

@XBlock.needs('user')
class CoConstructCPSXBlock(XBlock):
    """
    Add-on to the CPSXBlock which allows for co-constructed problems (those which require previous information for solutions)
    """

    provider_userA = String(
        default="", scope=Scope.settings,
        help="The target module for Version 1's \"Part 1\""
    )

    provider_userB = String(
        default="", scope=Scope.settings,
        help="The target module for Version 2's \"Part 1\""
    )

    receiver_userA = String(
        default="", scope=Scope.settings,
        help="The target module for the \"Part 2\" that requires information from both Versions' Part 1s"
    )

    receiver_userB = String(
        default="", scope=Scope.settings,
        help="The target module for the \"Part 2\" that requires information from both Versions' Part 1s"
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the CoConstructCPSXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/constructcpsxblock.html")
        frag = Fragment(html.format(self=self))
        # frag.add_css(selaf.resource_string("static/css/constructcpsxblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/constructcpsxblock.js"))

        # Actual init
        initdict = {
            'providerA': self.provider_userA, 
            'providerB': self.provider_userB, 
            'receiverA': self.receiver_userA,
            'receiverB': self.receiver_userB
        }

        frag.initialize_js('CoConstructCPSXBlock', initdict)
        return frag
    
    @property
    def course_id(self):
        if hasattr(self, 'xmodule_runtime'):
            if hasattr(self.xmodule_runtime.course_id, 'to_deprecated_string'):
                return self.xmodule_runtime.course_id.to_deprecated_string()
            else:
                return self.xmodule_runtime.course_id
        
        return 'course-v1:NYU+DEMO_101+2018_T1'
    
    @staticmethod
    def short_module_id(module):
        return re.match(r"problem\+block@(\w+)", module)
    
    @XBlock.json_handler
    def problem_submit(self, data):
        """
        Sends the server a notice that a receiver has been submitted
        """

        rec = data['receiver']
        assert (rec == self.receiver_userA) or (rec == self.receiver_userB) # Just in case

        uid = self.get_userid()

        if isinstance(uid, str):
            raise Exception("User not found")
        
        ans       = data['answer']
        total_ans = ""

        # Collect provided answers
        if rec == self.receiver_userA:
            user_pans    = self.get_user_provider_answer(uid, self.provider_userA)
            partner_pans = self.get_partner_provider_answer(uid, self.provider_userB)

            total_ans = self.format_total_answer(user_pans, partner_pans, ans)
        else:
            user_pans    = self.get_user_provider_answer(uid, self.provider_userB)
            partner_pans = self.get_partner_provider_answer(uid, self.provider_userA)

            total_ans = self.format_total_answer(partner_pans, user_pans, ans)
        
        # Send grader collected answers
        res = self.post_edx(rec, total_ans)

        return res.text
    
    def post_api(self, uri, json_data):
        return requests.post("{0}:{1}{2}".format(BASE_URL, PORT, uri), json=json_data)
    
    def post_edx(self, problem_module, data_string):
        url = "{0}/courses/{1}/xblock/{2}/handler/xmodule_handler/problem_check".format(BASE_URL, self.course_id, problem_module)
        key = "input_{}_2_1".format(CoConstructCPSXBlock.short_module_id(problem_module))

        return requests.post(url, json={key: data_string})
    
    def format_total_answer(self, provider_answer_A, provider_answer_B, receiver_ans):
        return json.dumps({"provider_A": provider_answer_A, "provider_B": provider_answer_B, "answer": receiver_ans})
        
    def get_partner_provider_answer(self, current_user, provider_module):
        """
        Fetches the answer for the partner's provider problem
        """
        data = {"curr_user": current_user, "problem_id": provider_module}

        res    = self.post_api("/sessions/getPartnerAnswerForProblem", data)
        resobj = json.loads(res.text)

        if "ans" not in resobj:
            raise Exception(resobj["err"])
        else:
            return resobj["ans"]
    
    def get_user_provider_answer(self, current_user, provider_module):
        """
        Fetches the answer for the user's provider problem
        """
        data = {"curr_user": current_user, "problem_id": provider_module}

        res    = self.post_api("/sessions/getUserAnswerForProblem", data)
        resobj = json.loads(res.text)

        if "ans" not in resobj:
            raise Exception(resobj["err"])
        else:
            return resobj["ans"]
    
    def get_user(self):
        """
        Get an attribute of the current user.
        """
        user_service = self.runtime.service(self, 'user')
        if user_service:
            # May be None when creating bok choy test fixtures
            return user_service.get_current_user()
        return None

    def get_userid(self):
        try:
            return self.get_user().opt_attrs['edx-platform.user_id']
        except Exception:
            return '4'

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("CoConstructCPSXBlock",
             """<constructcpsxblock/>
             """),
            ("Multiple CoConstructCPSXBlock",
             """<vertical_demo>
                <constructcpsxblock/>
                <constructcpsxblock/>
                <constructcpsxblock/>
                </vertical_demo>
             """),
        ]
