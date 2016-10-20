
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
import us.kbase.common.service.Tuple3;


/**
 * <p>Original spec-file type: CreateNewNarrativeParams</p>
 * <pre>
 * app - name of app (optional, either app or method may be defined)
 * method - name of method (optional, either app or method may be defined)
 * appparam - paramters of app/method packed into string in format:
 *     "step_pos,param_name,param_value(;...)*" (alternative to appData)
 * appData - parameters of app/method in unpacked form (alternative to appparam)
 * markdown - markdown text for cell of 'markdown' type (optional)
 * copydata - packed inport data in format "import(;...)*"
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "app",
    "method",
    "appparam",
    "appData",
    "markdown",
    "copydata"
})
public class CreateNewNarrativeParams {

    @JsonProperty("app")
    private java.lang.String app;
    @JsonProperty("method")
    private java.lang.String method;
    @JsonProperty("appparam")
    private java.lang.String appparam;
    @JsonProperty("appData")
    private List<Tuple3 <String, String, String>> appData;
    @JsonProperty("markdown")
    private java.lang.String markdown;
    @JsonProperty("copydata")
    private java.lang.String copydata;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("app")
    public java.lang.String getApp() {
        return app;
    }

    @JsonProperty("app")
    public void setApp(java.lang.String app) {
        this.app = app;
    }

    public CreateNewNarrativeParams withApp(java.lang.String app) {
        this.app = app;
        return this;
    }

    @JsonProperty("method")
    public java.lang.String getMethod() {
        return method;
    }

    @JsonProperty("method")
    public void setMethod(java.lang.String method) {
        this.method = method;
    }

    public CreateNewNarrativeParams withMethod(java.lang.String method) {
        this.method = method;
        return this;
    }

    @JsonProperty("appparam")
    public java.lang.String getAppparam() {
        return appparam;
    }

    @JsonProperty("appparam")
    public void setAppparam(java.lang.String appparam) {
        this.appparam = appparam;
    }

    public CreateNewNarrativeParams withAppparam(java.lang.String appparam) {
        this.appparam = appparam;
        return this;
    }

    @JsonProperty("appData")
    public List<Tuple3 <String, String, String>> getAppData() {
        return appData;
    }

    @JsonProperty("appData")
    public void setAppData(List<Tuple3 <String, String, String>> appData) {
        this.appData = appData;
    }

    public CreateNewNarrativeParams withAppData(List<Tuple3 <String, String, String>> appData) {
        this.appData = appData;
        return this;
    }

    @JsonProperty("markdown")
    public java.lang.String getMarkdown() {
        return markdown;
    }

    @JsonProperty("markdown")
    public void setMarkdown(java.lang.String markdown) {
        this.markdown = markdown;
    }

    public CreateNewNarrativeParams withMarkdown(java.lang.String markdown) {
        this.markdown = markdown;
        return this;
    }

    @JsonProperty("copydata")
    public java.lang.String getCopydata() {
        return copydata;
    }

    @JsonProperty("copydata")
    public void setCopydata(java.lang.String copydata) {
        this.copydata = copydata;
    }

    public CreateNewNarrativeParams withCopydata(java.lang.String copydata) {
        this.copydata = copydata;
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
        return ((((((((((((((("CreateNewNarrativeParams"+" [app=")+ app)+", method=")+ method)+", appparam=")+ appparam)+", appData=")+ appData)+", markdown=")+ markdown)+", copydata=")+ copydata)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
