<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<style type="text/css">
/*base css*/
    body
    {
      margin: 0px;
      padding: 15px;
    }

    body, td, th
    {
      font-family: "Lucida Grande", "Lucida Sans Unicode", Helvetica, Arial, Tahoma, sans-serif;
      font-size: 10pt;
    }

    th
    {
      text-align: left;
    }

    h1
    {
      margin-top: 0px;
    }
    a
    {
      color:#4a72af
    }
/*div styles*/

.status{background-color:<%= 
            build.result.toString() == "SUCCESS" ? 'green' : 'red' %>;font-size:28px;font-weight:bold;color:white;width:720px;height:52px;margin-bottom:18px;text-align:center;vertical-align:middle;border-collapse:collapse;background-repeat:no-repeat}
.status .info{color:white!important;text-shadow:0 -1px 0 rgba(0,0,0,0.3);font-size:32px;line-height:36px;padding:8px 0}
</style>
<body>
<div class="content round_border">
                <div class="status">
                        <p class="info">The build <%= build.result.toString().toLowerCase() %></p>
                </div>
                <!-- status -->
                        <table>
                                <tbody>
                                        <tr>
                                                <th>Project:</th>
                                                <td>${project.name}</td>
                                        </tr>
                                        <tr>
                                                <th>Build ${build.displayName}:</th>
                                                <td><a
                                                        href="${rooturl}${build.url}">${rooturl}${build.url}</a></td>
                                        </tr>
                                        <tr>
                                                <th>Date of build:</th>
                                                <td>${it.timestampString}</td>
                                        </tr>
                                        <tr>
                                                <th>Build duration:</th>
                                                <td>${build.durationString}</td>
                                        </tr>
                                        <tr>
                                                <td colspan="2">&nbsp;</td>
                                        </tr>
                                </tbody>

                        </table>
                <!-- main -->
        <% def artifacts = build.artifacts
            if(artifacts != null && artifacts.size() > 0) { %>

                        <b>Build Artifacts:</b>
                        <ul>
            <%          artifacts.each() { f -> %>
                <li><a href="${rooturl}${build.url}artifact/${f}">${f}</a></li>
            <%          } %>
                        </ul>
        <% } %>
  <!-- artifacts -->

<% 
  lastAllureReportBuildAction = build.getAction(ru.yandex.qatools.allure.jenkins.AllureReportBuildAction.class)
  lastAllureBuildAction = build.getAction(ru.yandex.qatools.allure.jenkins.AllureBuildAction.class)

  if (lastAllureReportBuildAction) {
    allureResultsUrl = "${rooturl}${build.url}allure"
    allureLastBuildSuccessRate = String.format("%.2f", lastAllureReportBuildAction.getPassedCount() * 100f / lastAllureReportBuildAction.getTotalCount())
  }
%>
<%
String authHeaderValue = "Basic " + "dmFubnRhOkplbmtpbnNAMjAyMw==";
content=new URL("${allureResultsUrl}/graph").getBytes( useCaches: true, allowUserInteraction: false, requestProperties: ["User-Agent": "Groovy Sample Script", "Authorization": authHeaderValue, "Content-Type": "image/png"])
%>
<% if (lastAllureReportBuildAction) { %>
<h2>Allure Results</h2>
<table>
            <tbody>
                        <tr>
                                    <th>Total Allure tests run:</th>
                                    <td><a href="${allureResultsUrl}">${lastAllureReportBuildAction.getTotalCount()}</a></td>
                        </tr>
                        <tr>
                                    <th>Failed:</th>
                                    <td>${lastAllureReportBuildAction.getFailedCount()} </td>
                        </tr>
                        <tr>
                                    <th>Passed:</th>
                                    <td>${lastAllureReportBuildAction.getPassedCount()} </td>
                        </tr>
                        <tr>
                                    <th>Skipped:</th>
                                    <td>${lastAllureReportBuildAction.getSkipCount()} </td>
                        </tr>
                        <tr>
                                    <th>Broken:</th>
                                    <td>${lastAllureReportBuildAction.getBrokenCount()} </td>
                        </tr>
                        <tr>
                                    <th>Success rate: </th>
                                    <td>${allureLastBuildSuccessRate}%  </td>
                        </tr>
                        <tr>
                          <th>Execution History:</th>
                          <td><a
                                 href="${rooturl}${build.url}allure">${rooturl}${build.url}allure</a></td>
                        <tr>

            </tbody>
</table>
<img src="data:image/png;base64, ${content.encodeBase64().toString()}"/>
<% } %>



  <!-- content -->
  <!-- bottom message -->
</body>