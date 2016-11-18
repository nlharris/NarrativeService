
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
 * <p>Original spec-file type: DataPaletteInfo</p>
 * <pre>
 * ref - reference to any DataPalette container pointing to given object,
 * refs - list of references to all DataPalette containers pointing to 
 *     given object.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "ref",
    "refs"
})
public class DataPaletteInfo {

    @JsonProperty("ref")
    private java.lang.String ref;
    @JsonProperty("refs")
    private List<String> refs;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("ref")
    public java.lang.String getRef() {
        return ref;
    }

    @JsonProperty("ref")
    public void setRef(java.lang.String ref) {
        this.ref = ref;
    }

    public DataPaletteInfo withRef(java.lang.String ref) {
        this.ref = ref;
        return this;
    }

    @JsonProperty("refs")
    public List<String> getRefs() {
        return refs;
    }

    @JsonProperty("refs")
    public void setRefs(List<String> refs) {
        this.refs = refs;
    }

    public DataPaletteInfo withRefs(List<String> refs) {
        this.refs = refs;
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
        return ((((((("DataPaletteInfo"+" [ref=")+ ref)+", refs=")+ refs)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
