
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
 * <p>Original spec-file type: CopyNarrativeParams</p>
 * <pre>
 * workspaceId - optional workspace ID, if not specified then 
 *     property from workspaceRef object info is used.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspaceRef",
    "workspaceId",
    "newName"
})
public class CopyNarrativeParams {

    @JsonProperty("workspaceRef")
    private String workspaceRef;
    @JsonProperty("workspaceId")
    private Long workspaceId;
    @JsonProperty("newName")
    private String newName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspaceRef")
    public String getWorkspaceRef() {
        return workspaceRef;
    }

    @JsonProperty("workspaceRef")
    public void setWorkspaceRef(String workspaceRef) {
        this.workspaceRef = workspaceRef;
    }

    public CopyNarrativeParams withWorkspaceRef(String workspaceRef) {
        this.workspaceRef = workspaceRef;
        return this;
    }

    @JsonProperty("workspaceId")
    public Long getWorkspaceId() {
        return workspaceId;
    }

    @JsonProperty("workspaceId")
    public void setWorkspaceId(Long workspaceId) {
        this.workspaceId = workspaceId;
    }

    public CopyNarrativeParams withWorkspaceId(Long workspaceId) {
        this.workspaceId = workspaceId;
        return this;
    }

    @JsonProperty("newName")
    public String getNewName() {
        return newName;
    }

    @JsonProperty("newName")
    public void setNewName(String newName) {
        this.newName = newName;
    }

    public CopyNarrativeParams withNewName(String newName) {
        this.newName = newName;
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
        return ((((((((("CopyNarrativeParams"+" [workspaceRef=")+ workspaceRef)+", workspaceId=")+ workspaceId)+", newName=")+ newName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
