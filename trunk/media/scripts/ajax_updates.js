/*
    EDSA Ajax update utilities
    Michael Price, Oct. 2010
    
    These functions allow DOM elements to submit arbitrary subsets of the forms
    on a page to an arbitrary URL, and allow the URL to add/modify/delete 
    sections of the page.  This is done using the generic function ajax_update
    or by calling one of these convenience functions:
      - update_form(request_path, form_id, form_div_id, command, post_load)
        Submits a form and waits for a response to update the <div> containing
        the form. This is useful if you want some fields of the form to be
        dependent on other fields.
      - add_pane(request_path, form_id, tab_id, command, target_id, target_label, post_load)
        Submits a form and creates a new tab (named target_id and labeled
        target_label) within the tab group specified by tab_id.  The response
        can populate the new tab with content.
      - save_pane(request_path, form_ids, tab_id, command, target_id, post_load)
        Submits one or more forms and allows multiple targets to be updated.
        The tab specified in target_id can be updated or closed.  To allow
        multiple targets to be updated, replace target_id with an object whose
        keys include 'default' (the meaning of different keys needs to be 
        synchronized with the server-side view code).
    Usage notes:
      - Take a look at examples in the rendered HTML code of EDSA pages for 
        suggestions on how to use these functions.
      - In all cases the post_load argument, which is a function handle to be
        executed after the Ajax operation, is optional.

*/


//  Generic handler for Ajax requests involving forms
function ajax_update(request_path, form_ids, tab_id, command, targets, post_load, add_pane_label, save_pane)
{
    console.log("Ajax update: command = " + command + ", form_ids = " + JSON.stringify(form_ids) + ", tab_id = " + JSON.stringify(tab_id) + ", targets = " + JSON.stringify(targets) + ", add_pane_label = " + add_pane_label + ",) save_pane = " + save_pane);
    
    //  The targets variable (as submitted) is an object containing key/value pairs.
    //  If a string is provided, reformat it as an object with the key 'default'.
    if (dojo.isString(targets))
    {
        default_target_id = targets;
        targets = {default: default_target_id};
    }
    else
    {
        default_target_id = targets["default"];
    }
    
    //  If you are adding or saving a pane, that pane's div ID must be the default.
    //  Other panes that need updating can be included as non-default targets.
    if (add_pane_label)
    {
        //  Create a new tab if desired.
        var parent = dijit.byId(tab_id);
        var new_pane = new dijit.layout.ContentPane({
            title: add_pane_label,
            content: 'Loading...',
            id: default_target_id,
            closable: "true"
        });
        parent.addChild(new_pane);
    }
    
    //  Prepare an object to be JSON-encoded and submitted.
    var content_dict = {};
    content_dict['command'] = command;
    content_dict['target'] = dojo.toJson(targets);
    content_dict['forms'] = {};
    form_dict = {};
    for (var i = 0; i < form_ids.length; i++)
    {
        form_dict[form_ids[i]] = dojo.formToObject(form_ids[i]);
    }
    content_dict['forms'] = dojo.toJson(form_dict);

    //  Prepare an Ajax request.
    var xhrArgs = {
        url: request_path + 'ajax_update',
        handleAs:'json',
        content: content_dict,
        load: function(data){
            //  console.log("Got savepane response - parsing " + form_ids);
            var updated_ids = apply_fragment_changes(data);
            
            //  Close the pane if it isn't needed
            if (save_pane)
            {
                if (!in_array(updated_ids, default_target_id))
                {
                    //  console.log("Success; closing pane " + default_target_id);
                    dijit.byId(tab_id).removeChild(dijit.byId(default_target_id));
                    dijit.byId(default_target_id).destroyDescendants();
                    dijit.byId(default_target_id).destroy();
                    
                    //  Select a child tab that has been updated if there is one
                    if (updated_ids.length > 0)
                        dijit.byId(tab_id).selectChild(dijit.byId(updated_ids[0]))
                }
            }
            if (post_load)
            {
                //  console.log("Running post_load callback " + post_load);
                post_load();
            }
        }
    };
        
    //  Submit an Ajax request.
    var deferred = dojo.xhrGet(xhrArgs);
    
    //  Transfer focus to a new tab if one has been created.
    if (add_pane_label)
        parent.selectChild(dijit.byId(default_target_id)); 
}


/*  Convenience functions   */

//  Submit a request that updates the supplied form in place.
function update_form(request_path, form_id, form_div_id, command, post_load)
{
    if (form_id instanceof Array)
    {
        ajax_update(request_path, form_id, null, command, form_div_id, post_load, false, false);
    }
    else
    {
        ajax_update(request_path, [form_id], null, command, form_div_id, post_load, false, false);
    }
}

//  Submit a request that causes a new tab to be added in the content pane
function add_pane(request_path, form_id, tab_id, command, target_id, target_label, post_load)
{
    ajax_update(request_path, [form_id], tab_id, command, target_id, post_load, target_label, false);
}

//  Submit a request that causes a tab to be closed if it is not updated by the response
function save_pane(request_path, form_ids, tab_id, command, target_id, post_load)
{
    ajax_update(request_path, form_ids, tab_id, command, target_id, post_load, false, true);
}