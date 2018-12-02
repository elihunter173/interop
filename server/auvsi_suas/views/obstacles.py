"""Interoperability obstacles view."""

import iso8601
import json
import logging
from auvsi_suas.views.decorators import require_login
from auvsi_suas.views.missions import active_mission
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.generic import View

logger = logging.getLogger(__name__)


class Obstacles(View):
    """Gets the obstacle information as JSON with a GET request."""

    @method_decorator(require_login)
    def dispatch(self, *args, **kwargs):
        return super(Obstacles, self).dispatch(*args, **kwargs)

    def get(self, request):
        # Get active mission for forming responses.
        (mission, err) = active_mission()
        if err:
            return err

        # Form JSON response portion for stationary obstacles
        stationary_obstacles = mission.stationary_obstacles.select_related(
        ).all().order_by('pk')
        stationary_obstacles_json = []
        for cur_obst in stationary_obstacles:
            # Add current obstacle
            cur_obst_json = cur_obst.json()
            stationary_obstacles_json.append(cur_obst_json)

        # Form final JSON response
        data = {
            'stationary_obstacles': stationary_obstacles_json,
        }

        # Return JSON data
        return HttpResponse(json.dumps(data), content_type="application/json")
