
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
 * <p>Original spec-file type: ListObjectsWithSetsOutput</p>
 * <pre>
 * data_palette_refs - mapping from workspace Id to reference to DataPalette
 *     container existing in given workspace.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "data",
    "data_palette_refs"
})
public class ListObjectsWithSetsOutput {

    @JsonProperty("data")
    private List<ListItem> data;
    @JsonProperty("data_palette_refs")
    private Map<String, String> dataPaletteRefs;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("data")
    public List<ListItem> getData() {
        return data;
    }

    @JsonProperty("data")
    public void setData(List<ListItem> data) {
        this.data = data;
    }

    public ListObjectsWithSetsOutput withData(List<ListItem> data) {
        this.data = data;
        return this;
    }

    @JsonProperty("data_palette_refs")
    public Map<String, String> getDataPaletteRefs() {
        return dataPaletteRefs;
    }

    @JsonProperty("data_palette_refs")
    public void setDataPaletteRefs(Map<String, String> dataPaletteRefs) {
        this.dataPaletteRefs = dataPaletteRefs;
    }

    public ListObjectsWithSetsOutput withDataPaletteRefs(Map<String, String> dataPaletteRefs) {
        this.dataPaletteRefs = dataPaletteRefs;
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
        return ((((((("ListObjectsWithSetsOutput"+" [data=")+ data)+", dataPaletteRefs=")+ dataPaletteRefs)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
