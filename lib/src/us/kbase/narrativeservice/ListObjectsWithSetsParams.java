
package us.kbase.narrativeservice;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: ListObjectsWithSetsParams</p>
 * <pre>
 * ws_name/ws_id/workspaces - alternative way of defining workspaces (in
 *     case of 'workspaces' each string could be workspace name or ID
 *     converted into string).
 * types - optional filter field, limiting output list to set of types.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "ws_name",
    "ws_id",
    "workspaces",
    "types"
})
public class ListObjectsWithSetsParams {

    @JsonProperty("ws_name")
    private java.lang.String wsName;
    @JsonProperty("ws_id")
    private Long wsId;
    @JsonProperty("workspaces")
    private List<String> workspaces;
    @JsonProperty("types")
    private List<String> types;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("ws_name")
    public java.lang.String getWsName() {
        return wsName;
    }

    @JsonProperty("ws_name")
    public void setWsName(java.lang.String wsName) {
        this.wsName = wsName;
    }

    public ListObjectsWithSetsParams withWsName(java.lang.String wsName) {
        this.wsName = wsName;
        return this;
    }

    @JsonProperty("ws_id")
    public Long getWsId() {
        return wsId;
    }

    @JsonProperty("ws_id")
    public void setWsId(Long wsId) {
        this.wsId = wsId;
    }

    public ListObjectsWithSetsParams withWsId(Long wsId) {
        this.wsId = wsId;
        return this;
    }

    @JsonProperty("workspaces")
    public List<String> getWorkspaces() {
        return workspaces;
    }

    @JsonProperty("workspaces")
    public void setWorkspaces(List<String> workspaces) {
        this.workspaces = workspaces;
    }

    public ListObjectsWithSetsParams withWorkspaces(List<String> workspaces) {
        this.workspaces = workspaces;
        return this;
    }

    @JsonProperty("types")
    public List<String> getTypes() {
        return types;
    }

    @JsonProperty("types")
    public void setTypes(List<String> types) {
        this.types = types;
    }

    public ListObjectsWithSetsParams withTypes(List<String> types) {
        this.types = types;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((("ListObjectsWithSetsParams"+" [wsName=")+ wsName)+", wsId=")+ wsId)+", workspaces=")+ workspaces)+", types=")+ types)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
