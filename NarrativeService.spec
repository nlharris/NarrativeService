/*
A KBase module: NarrativeService
*/

module NarrativeService {


    /* 
        A time in the format YYYY-MM-DDThh:mm:ssZ, where Z is either the
        character Z (representing the UTC timezone) or the difference
        in time to UTC in the format +/-HHMM, eg:
            2012-12-17T23:24:06-0500 (EST time)
            2013-04-03T08:56:32+0000 (UTC time)
            2013-04-03T08:56:32Z (UTC time)
    */
    typedef string timestamp;

    /* Represents the permissions a user or users have to a workspace:
        
        'a' - administrator. All operations allowed.
        'w' - read/write.
        'r' - read.
        'n' - no permissions.
    */
    typedef string permission;

    /* The lock status of a workspace.
        One of 'unlocked', 'locked', or 'published'.
    */
    typedef string lock_status;

    /* Information about an object, including user provided metadata.
        
        obj_id objid - the numerical id of the object.
        obj_name name - the name of the object.
        type_string type - the type of the object.
        timestamp save_date - the save date of the object.
        obj_ver ver - the version of the object.
        username saved_by - the user that saved or copied the object.
        ws_id wsid - the workspace containing the object.
        ws_name workspace - the workspace containing the object.
        string chsum - the md5 checksum of the object.
        int size - the size of the object in bytes.
        usermeta meta - arbitrary user-supplied metadata about
            the object.
    */
    typedef tuple<int objid, string name, string type,
        timestamp save_date, int version, string saved_by,
        int wsid, string workspace, string chsum, int size,
        mapping<string, string> meta> object_info;

    typedef structure {
        list<object_info> set_items_info;
    } SetItems;

    /*
        object_info - workspace info for object (including set object),
        set_items - optional property listing info for items of set object
    */
    typedef structure {
        object_info object_info;
        SetItems set_items;
    } ListItem;

    typedef structure {
        string ws_name;
        int ws_id;
    } ListObjectsWithSetsParams;

    typedef structure {
        list<ListItem> data;
    } ListObjectsWithSetsOutput;

    funcdef list_objects_with_sets(ListObjectsWithSetsParams params)
        returns (ListObjectsWithSetsOutput) authentication required;

};
