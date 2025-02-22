# -*- coding: utf-8 -*-

# Copyright (c) 2015 CoNWeT Lab., Universidad Politécnica de Madrid

# This file is part of CKAN Data Requests Extension.

# CKAN Data Requests Extension is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# CKAN Data Requests Extension is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with CKAN Data Requests Extension. If not, see <http://www.gnu.org/licenses/>.

from ckan import authz
from ckan.plugins.toolkit import asbool, auth_disallow_anonymous_access, config, get_action

from . import constants


def create_datarequest(context, data_dict):
    return {
        'success': asbool(config.get("ckanext.auth.create_datarequest_if_not_in_organization", "True"))
        or _is_any_group_member(context)
    }


def _is_any_group_member(context):
    user_name = context.get('user')
    if not user_name:
        user_obj = context.get('auth_user_obj')
        if user_obj:
            user_name = user_obj.name
    return user_name and authz.has_user_permission_for_some_org(user_name, 'read')


@auth_disallow_anonymous_access
def show_datarequest(context, data_dict):
    return {'success': True}


def auth_if_creator(context, data_dict, show_function):
    # Sometimes data_dict only contains the 'id'
    if 'user_id' not in data_dict:
        function = get_action(show_function)
        data_dict = function({'ignore_auth': True}, {'id': data_dict.get('id')})

    return {'success': data_dict['user_id'] == context.get('auth_user_obj').id}


def update_datarequest(context, data_dict):
    return auth_if_creator(context, data_dict, constants.SHOW_DATAREQUEST)


@auth_disallow_anonymous_access
def list_datarequests(context, data_dict):
    return {'success': True}


def delete_datarequest(context, data_dict):
    return auth_if_creator(context, data_dict, constants.SHOW_DATAREQUEST)


def close_datarequest(context, data_dict):
    return auth_if_creator(context, data_dict, constants.SHOW_DATAREQUEST)


def comment_datarequest(context, data_dict):
    return {'success': True}


@auth_disallow_anonymous_access
def list_datarequest_comments(context, data_dict):
    new_data_dict = {'id': data_dict['datarequest_id']}
    return show_datarequest(context, new_data_dict)


@auth_disallow_anonymous_access
def show_datarequest_comment(context, data_dict):
    return {'success': True}


def update_datarequest_comment(context, data_dict):
    return auth_if_creator(context, data_dict, constants.SHOW_DATAREQUEST_COMMENT)


def delete_datarequest_comment(context, data_dict):
    return auth_if_creator(context, data_dict, constants.SHOW_DATAREQUEST_COMMENT)


def follow_datarequest(context, data_dict):
    return {'success': True}


def unfollow_datarequest(context, data_dict):
    return {'success': True}
