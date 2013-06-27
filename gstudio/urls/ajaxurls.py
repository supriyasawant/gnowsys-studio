
# Copyright (c) 2011,  2012 Free Software Foundation

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""Urls for the Gstudio sitemap"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

urlpatterns = patterns('gstudio.views.ajaxviews',
                       url(r'^ajaxattribute/$', 'AjaxAttribute',name='ajax_views'),
                       url(r'^relation/add/ajaxleft/$', 'AjaxRelationleft',name='ajax_relnleft_views'),
		       url(r'^relation/add/ajaxright/$', 'AjaxRelationright',name='ajax_relnright_views'),
		       url(r'^relation/ajaxleft/$', 'AjaxRelationleft',name='ajax_relnleft_views'),
		       url(r'^relation/ajaxright/$', 'AjaxRelationright',name='ajax_relnright_views'),
 		       url(r'^contentorgadd/$', 'AjaxAddContentOrg', name='ajax_views_contentorgadd'),
                       url(r'^ajaxcreatehtml/$', 'AjaxCreateHtml', name='ajax_views_createhtml'),
                       url(r'^ajaxcreatefile/$', 'AjaxCreateFile', name='ajax_views_createfile'),
                       url(r'^contentadd/$', 'AjaxAddContent', name='ajax_views_contentadd'),
		       url(r'^draweradd/$', 'AjaxAddDrawer', name='ajax_views_draweradd'),
                       url(r'^preview/$', 'Preview', name='ajax_views_preview'),
                       url(r'^status/$', 'Status', name='ajax_views_status'),
                       url(r'^pagedelete/$', 'Pagedelete', name='ajax_views_pagedelete'),

                       url(r'^htmlexport/$', 'HtmlExport', name='ajax_view_htmlexport'),
                       url(r'^collectionadd/$', 'AjaxAddCollection', name='ajax_view_collectionadd'),
                       url(r'^iswiki/$', 'IsWiki', name='ajax_view_iswiki'),
                       url(r'^deletepriorpage/$', 'ajaxDeletePriorpage', name='ajax_delete_priorpage'),
                       url(r'^addresponsestotwist/$', 'ajaxAddResponsesToTwist', name='ajax_addresponsestotwist'),
		       url(r'^userListForInvitation/$', 'ajaxuserListForInvitation', name='ajax_userListForInvitation'),
                       url(r'^sendInvitation/$', 'ajaxSendInvitation', name='ajax_SendInvitation'),
                       url(r'^releaseBlockResponseOfTwist/$', 'ajaxReleaseBlockResponseOfTwist', name='ajax_ReleaseBlockResponseOfTwist'),
                       url(r'^ajaxResponseReciev/$', 'ajaxResponseReciev', name='ajax_ajaxResponseReciev')
                       )
