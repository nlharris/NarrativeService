
package us.kbase.narrativeservice;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.Tuple11;


/**
 * <p>Original spec-file type: ListItem</p>
 * <pre>
 * object_info - workspace info for object (including set object),
 * set_items - optional property listing info for items of set object,
 * dp_info - optional data-palette info (defined for items stored in
 *     DataPalette object).
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "object_info",
    "set_items",
    "dp_info"
})
public class ListItem {

    @JsonProperty("object_info")
    private Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>> objectInfo;
    /**
     * <p>Original spec-file type: SetItems</p>
     * 
     * 
     */
    @JsonProperty("set_items")
    private SetItems setItems;
    /**
     * <p>Original spec-file type: DataPaletteInfo</p>
     * <pre>
     * ref - reference to DataPalette container pointing to given object.
     * </pre>
     * 
     */
    @JsonProperty("dp_info")
    private DataPaletteInfo dpInfo;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("object_info")
    public Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>> getObjectInfo() {
        return objectInfo;
    }

    @JsonProperty("object_info")
    public void setObjectInfo(Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>> objectInfo) {
        this.objectInfo = objectInfo;
    }

    public ListItem withObjectInfo(Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>> objectInfo) {
        this.objectInfo = objectInfo;
        return this;
    }

    /**
     * <p>Original spec-file type: SetItems</p>
     * 
     * 
     */
    @JsonProperty("set_items")
    public SetItems getSetItems() {
        return setItems;
    }

    /**
     * <p>Original spec-file type: SetItems</p>
     * 
     * 
     */
    @JsonProperty("set_items")
    public void setSetItems(SetItems setItems) {
        this.setItems = setItems;
    }

    public ListItem withSetItems(SetItems setItems) {
        this.setItems = setItems;
        return this;
    }

    /**
     * <p>Original spec-file type: DataPaletteInfo</p>
     * <pre>
     * ref - reference to DataPalette container pointing to given object.
     * </pre>
     * 
     */
    @JsonProperty("dp_info")
    public DataPaletteInfo getDpInfo() {
        return dpInfo;
    }

    /**
     * <p>Original spec-file type: DataPaletteInfo</p>
     * <pre>
     * ref - reference to DataPalette container pointing to given object.
     * </pre>
     * 
     */
    @JsonProperty("dp_info")
    public void setDpInfo(DataPaletteInfo dpInfo) {
        this.dpInfo = dpInfo;
    }

    public ListItem withDpInfo(DataPaletteInfo dpInfo) {
        this.dpInfo = dpInfo;
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
        return ((((((((("ListItem"+" [objectInfo=")+ objectInfo)+", setItems=")+ setItems)+", dpInfo=")+ dpInfo)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
