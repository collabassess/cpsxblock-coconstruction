import re
import json
import logging

import pkg_resources
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String
from xblock.fragment import Fragment
from xblockutils.studio_editable import StudioEditableXBlockMixin

import requests

log = logging.getLogger(__name__)

@XBlock.needs('user')
class CoConstructCPSXBlock(StudioEditableXBlockMixin, XBlock):
    """
    Add-on to the CPSXBlock which allows for co-constructed problems (those which require previous information for solutions)
    """

    api_host = String(
        default="localhost", scope=Scope.settings,
        help="Location of the CPSX API (most likely localhost)"
    )

    api_port = Integer(
        default=3000, scope=Scope.settings,
        help="Port on which the CPSX API is listening"
    )

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

    editable_fields = (
        "api_host",
        "api_port",
        "provider_userA",
        "provider_userB",
        "receiver_userA",
        "receiver_userB"
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")
    
    display_name = String(
        display_name="CoConstructCPSXBlock",
        help="Enables co-constructed, context-dependent items for collaborative problem solving",
        scope=Scope.settings,
        default="CoConstructCPSXBlock"
    )

    def student_view(self, context=None):
        """
        The primary view of the CoConstructCPSXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/constructcpsxblock.html")
        frag = Fragment(html.format(self=self))
        # No styling needed
        # frag.add_css(selaf.resource_string("static/css/constructcpsxblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/constructcpsxblock.js"))

        # Pass module IDs to the JS source file
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
    
    @staticmethod
    def smart_cast(answer):
        """
        Determine if answer is int, float, complex, or string. 
        Defaults to string for structurally complex answers.
        """
        if isinstance(answer, str):
            work = answer

            # Check to see if answer is escaped
            if re.match(r"\"\d+\"|\"\d+\.\d+\"|\\\"\d+\\\"|\\\"\d+\.\d+\\\"", work) is not None:
                work = work.replace("\"", "")

            try:
                test = int(work)
                return test
            except ValueError:
                try:
                    test = float(work)
                    return test
                except ValueError:
                    try:
                        test = complex(work)
                        return test
                    except ValueError:
                        return work
        else:
            # Don't need to bother typecasting
            return answer
    
    @XBlock.json_handler
    def problem_submit(self, data, suffix=""):
        """
        Sends the server a notice that a receiver has been submitted
        """

        rec = data['receiver']
        assert (rec == self.receiver_userA) or (rec == self.receiver_userB) # Just in case

        uid = self.get_userid()

        # Catches the "return '4'" thing found below in get_userid()
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
        
        return {"answer": total_ans, "course_id": self.course_id, "problem": rec}
    
    def post_api(self, uri, json_data):
        """
        Submit query to the CPSX API
        """
        return requests.post("http://{0}:{1}{2}".format(self.api_host, self.api_port, uri), json=json_data)
    
    def format_total_answer(self, provider_answer_A, provider_answer_B, receiver_ans):
        return {
            "provider_A": CoConstructCPSXBlock.smart_cast(provider_answer_A), 
            "provider_B": CoConstructCPSXBlock.smart_cast(provider_answer_B), 
            "answer": CoConstructCPSXBlock.smart_cast(receiver_ans)
        }
        
    def get_partner_provider_answer(self, current_user, provider_module):
        """
        Fetches the answer for the partner's provider problem
        """
        data = {"curr_user": current_user, "problem_id": str(provider_module)}

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
        data = {"curr_user": current_user, "problem_id": str(provider_module)}

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
            # This return statement is copied from collabassess/CPSXblock. I have no idea why '4' was chosen.
            return '4'

    @staticmethod
    def workbench_scenarios():
        """
        A canned scenario for display in the workbench. Only renders for the XBlock SDK.
        """
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
