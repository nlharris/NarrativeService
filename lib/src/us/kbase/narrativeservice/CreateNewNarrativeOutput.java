
package us.kbase.narrativeservice;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: CreateNewNarrativeOutput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspaceInfo",
    "objectInfo"
})
public class CreateNewNarrativeOutput {

    /**
     * <p>Original spec-file type: WorkspaceInfo</p>
     * <pre>
     * Restructured workspace info 'wsInfo' tuple:
     * id: wsInfo[0],
     * name: wsInfo[1],
     * owner: wsInfo[2],
     * moddate: wsInfo[3],
     * object_count: wsInfo[4],
     * user_permission: wsInfo[5],
     * globalread: wsInfo[6],
     * lockstat: wsInfo[7],
     * metadata: wsInfo[8],
     * modDate: no_timezone(wsInfo[3])
     * </pre>
     * 
     */
    @JsonProperty("workspaceInfo")
    private WorkspaceInfo workspaceInfo;
    /**
     * <p>Original spec-file type: ObjectInfo</p>
     * <pre>
     * Restructured workspace object info 'data' tuple:
     * id: data[0],
     * name: data[1],
     * type: data[2],
     * save_date: data[3],
     * version: data[4],
     * saved_by: data[5],
     * wsid: data[6],
     * ws: data[7],
     * checksum: data[8],
     * size: data[9],
     * metadata: data[10],
     * ref: data[6] + '/' + data[0] + '/' + data[4],
     * obj_id: 'ws.' + data[6] + '.obj.' + data[0],
     * typeModule: type[0],
     * typeName: type[1],
     * typeMajorVersion: type[2],
     * typeMinorVersion: type[3],
     * saveDateNoTZ: no_timezone(data[3])
     * </pre>
     * 
     */
    @JsonProperty("objectInfo")
    private ObjectInfo objectInfo;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
     * <p>Original spec-file type: WorkspaceInfo</p>
     * <pre>
     * Restructured workspace info 'wsInfo' tuple:
     * id: wsInfo[0],
     * name: wsInfo[1],
     * owner: wsInfo[2],
     * moddate: wsInfo[3],
     * object_count: wsInfo[4],
     * user_permission: wsInfo[5],
     * globalread: wsInfo[6],
     * lockstat: wsInfo[7],
     * metadata: wsInfo[8],
     * modDate: no_timezone(wsInfo[3])
     * </pre>
     * 
     */
    @JsonProperty("workspaceInfo")
    public WorkspaceInfo getWorkspaceInfo() {
        return workspaceInfo;
    }

    /**
     * <p>Original spec-file type: WorkspaceInfo</p>
     * <pre>
     * Restructured workspace info 'wsInfo' tuple:
     * id: wsInfo[0],
     * name: wsInfo[1],
     * owner: wsInfo[2],
     * moddate: wsInfo[3],
     * object_count: wsInfo[4],
     * user_permission: wsInfo[5],
     * globalread: wsInfo[6],
     * lockstat: wsInfo[7],
     * metadata: wsInfo[8],
     * modDate: no_timezone(wsInfo[3])
     * </pre>
     * 
     */
    @JsonProperty("workspaceInfo")
    public void setWorkspaceInfo(WorkspaceInfo workspaceInfo) {
        this.workspaceInfo = workspaceInfo;
    }

    public CreateNewNarrativeOutput withWorkspaceInfo(WorkspaceInfo workspaceInfo) {
        this.workspaceInfo = workspaceInfo;
        return this;
    }

    /**
     * <p>Original spec-file type: ObjectInfo</p>
     * <pre>
     * Restructured workspace object info 'data' tuple:
     * id: data[0],
     * name: data[1],
     * type: data[2],
     * save_date: data[3],
     * version: data[4],
     * saved_by: data[5],
     * wsid: data[6],
     * ws: data[7],
     * checksum: data[8],
     * size: data[9],
     * metadata: data[10],
     * ref: data[6] + '/' + data[0] + '/' + data[4],
     * obj_id: 'ws.' + data[6] + '.obj.' + data[0],
     * typeModule: type[0],
     * typeName: type[1],
     * typeMajorVersion: type[2],
     * typeMinorVersion: type[3],
     * saveDateNoTZ: no_timezone(data[3])
     * </pre>
     * 
     */
    @JsonProperty("objectInfo")
    public ObjectInfo getObjectInfo() {
        return objectInfo;
    }

    /**
     * <p>Original spec-file type: ObjectInfo</p>
     * <pre>
     * Restructured workspace object info 'data' tuple:
     * id: data[0],
     * name: data[1],
     * type: data[2],
     * save_date: data[3],
     * version: data[4],
     * saved_by: data[5],
     * wsid: data[6],
     * ws: data[7],
     * checksum: data[8],
     * size: data[9],
     * metadata: data[10],
     * ref: data[6] + '/' + data[0] + '/' + data[4],
     * obj_id: 'ws.' + data[6] + '.obj.' + data[0],
     * typeModule: type[0],
     * typeName: type[1],
     * typeMajorVersion: type[2],
     * typeMinorVersion: type[3],
     * saveDateNoTZ: no_timezone(data[3])
     * </pre>
     * 
     */
    @JsonProperty("objectInfo")
    public void setObjectInfo(ObjectInfo objectInfo) {
        this.objectInfo = objectInfo;
    }

    public CreateNewNarrativeOutput withObjectInfo(ObjectInfo objectInfo) {
        this.objectInfo = objectInfo;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((("CreateNewNarrativeOutput"+" [workspaceInfo=")+ workspaceInfo)+", objectInfo=")+ objectInfo)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
