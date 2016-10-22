
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
 * <p>Original spec-file type: CopyObjectParams</p>
 * <pre>
 * ref - workspace reference to source object,
 * target_ws_id/target_ws_name - alternative ways to define target workspace,
 * target_name - optional target object name (if not set then source object
 *     name is used).
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "ref",
    "target_ws_id",
    "target_ws_name",
    "target_name"
})
public class CopyObjectParams {

    @JsonProperty("ref")
    private String ref;
    @JsonProperty("target_ws_id")
    private Long targetWsId;
    @JsonProperty("target_ws_name")
    private String targetWsName;
    @JsonProperty("target_name")
    private String targetName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("ref")
    public String getRef() {
        return ref;
    }

    @JsonProperty("ref")
    public void setRef(String ref) {
        this.ref = ref;
    }

    public CopyObjectParams withRef(String ref) {
        this.ref = ref;
        return this;
    }

    @JsonProperty("target_ws_id")
    public Long getTargetWsId() {
        return targetWsId;
    }

    @JsonProperty("target_ws_id")
    public void setTargetWsId(Long targetWsId) {
        this.targetWsId = targetWsId;
    }

    public CopyObjectParams withTargetWsId(Long targetWsId) {
        this.targetWsId = targetWsId;
        return this;
    }

    @JsonProperty("target_ws_name")
    public String getTargetWsName() {
        return targetWsName;
    }

    @JsonProperty("target_ws_name")
    public void setTargetWsName(String targetWsName) {
        this.targetWsName = targetWsName;
    }

    public CopyObjectParams withTargetWsName(String targetWsName) {
        this.targetWsName = targetWsName;
        return this;
    }

    @JsonProperty("target_name")
    public String getTargetName() {
        return targetName;
    }

    @JsonProperty("target_name")
    public void setTargetName(String targetName) {
        this.targetName = targetName;
    }

    public CopyObjectParams withTargetName(String targetName) {
        this.targetName = targetName;
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
        return ((((((((((("CopyObjectParams"+" [ref=")+ ref)+", targetWsId=")+ targetWsId)+", targetWsName=")+ targetWsName)+", targetName=")+ targetName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
