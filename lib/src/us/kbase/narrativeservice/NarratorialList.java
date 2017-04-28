
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
 * <p>Original spec-file type: NarratorialList</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "narratorials"
})
public class NarratorialList {

    @JsonProperty("narratorials")
    private List<Narratorial> narratorials;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("narratorials")
    public List<Narratorial> getNarratorials() {
        return narratorials;
    }

    @JsonProperty("narratorials")
    public void setNarratorials(List<Narratorial> narratorials) {
        this.narratorials = narratorials;
    }

    public NarratorialList withNarratorials(List<Narratorial> narratorials) {
        this.narratorials = narratorials;
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
        return ((((("NarratorialList"+" [narratorials=")+ narratorials)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
