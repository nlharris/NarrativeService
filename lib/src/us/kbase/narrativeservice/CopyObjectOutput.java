
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
 * <p>Original spec-file type: CopyObjectOutput</p>
 * <pre>
 * info - workspace info of created object
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "info"
})
public class CopyObjectOutput {

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
     * saveDateMs: ServiceUtils.iso8601ToMillisSinceEpoch(data[3])
     * </pre>
     * 
     */
    @JsonProperty("info")
    private ObjectInfo info;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

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
     * saveDateMs: ServiceUtils.iso8601ToMillisSinceEpoch(data[3])
     * </pre>
     * 
     */
    @JsonProperty("info")
    public ObjectInfo getInfo() {
        return info;
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
     * saveDateMs: ServiceUtils.iso8601ToMillisSinceEpoch(data[3])
     * </pre>
     * 
     */
    @JsonProperty("info")
    public void setInfo(ObjectInfo info) {
        this.info = info;
    }

    public CopyObjectOutput withInfo(ObjectInfo info) {
        this.info = info;
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
        return ((((("CopyObjectOutput"+" [info=")+ info)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
