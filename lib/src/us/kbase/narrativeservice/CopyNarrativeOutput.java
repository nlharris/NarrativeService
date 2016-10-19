
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
 * <p>Original spec-file type: CopyNarrativeOutput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "newWsId",
    "newNarId"
})
public class CopyNarrativeOutput {

    @JsonProperty("newWsId")
    private Long newWsId;
    @JsonProperty("newNarId")
    private Long newNarId;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("newWsId")
    public Long getNewWsId() {
        return newWsId;
    }

    @JsonProperty("newWsId")
    public void setNewWsId(Long newWsId) {
        this.newWsId = newWsId;
    }

    public CopyNarrativeOutput withNewWsId(Long newWsId) {
        this.newWsId = newWsId;
        return this;
    }

    @JsonProperty("newNarId")
    public Long getNewNarId() {
        return newNarId;
    }

    @JsonProperty("newNarId")
    public void setNewNarId(Long newNarId) {
        this.newNarId = newNarId;
    }

    public CopyNarrativeOutput withNewNarId(Long newNarId) {
        this.newNarId = newNarId;
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
        return ((((((("CopyNarrativeOutput"+" [newWsId=")+ newWsId)+", newNarId=")+ newNarId)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
