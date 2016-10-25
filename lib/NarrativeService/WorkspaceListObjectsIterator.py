

class WorkspaceListObjectsIterator:

    # ws_info - optional workspace info tuple (if is not defined then either ws_id 
    #    or ws_name should be provided),
    # ws_id/ws_name - optional workspace identification (if neither is defined 
    #    then ws_info should be provided),
    # list_objects_params - optional structure with such Woskspace.ListObjectsParams 
    #    as 'type' or 'before', 'after', 'showHidden', 'includeMetadata' and so on,
    #    wherein there is no need to set 'ids' or 'workspaces' or 'min/maxObjectID'.
    def __init__(self, ws_client, ws_info = None, ws_id = None, ws_name = None, 
                 list_objects_params = {}, part_size = 10000):
        self.ws = ws_client
        if not ws_info:
            if (not ws_id) and (not ws_name):
                raise ValueError("In case ws_info is not set either ws_id or " +
                                 "ws_name should be set")
            ws_info = self.ws.get_workspace_info({"id": ws_id, "workspace": ws_name})
        if not ws_id:
            ws_id = ws_info[0]
        if not ws_name:
            ws_name = ws_info[1]
        self.max_obj_count = ws_info[4]
        list_objects_params['ids'] = [ws_id]
        list_objects_params['workspaces'] = [ws_name]
        self.list_objects_params = list_objects_params
        self.min_obj_id = 1
        self.part_size = part_size
        self.part_iter = self._load_next_part()
        pass

    # iterator implementation
    def __iter__(self):
        return self

    def next(self):
        while self.part_iter is not None:
            try:
                return self.part_iter.next()
            except StopIteration:
                self.part_iter = self._load_next_part()
        raise StopIteration

    def _load_next_part(self):
        if self.min_obj_id > self.max_obj_count:
            return None
        max_obj_id = self.min_obj_id + self.part_size - 1
        self.list_objects_params['minObjectID'] = self.min_obj_id
        self.list_objects_params['maxObjectID'] = max_obj_id
        self.min_obj_id += self.part_size  # For next load cycle
        return self.ws.list_objects(self.list_objects_params).__iter__()
