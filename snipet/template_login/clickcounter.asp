<%@ Language=VBScript %>
<!-- #include file=conn/dbcon.inc -->

<%
    <!-- sql_insert: click counter(Ajax) -->
    set con = Server.CreateObject("ADODB.Connection")
    con.Open Connect_db_IR()
    ip = Request.ServerVariables("REMOTE_ADDR")
    filename = Request.Form("filename")
    editSql = "INSERT INTO hbcpotal_count (access_ip, category, note, created_at) VALUES ('{ip}', 'linkclick', '{filename}', GETDATE())"
    editSql = Replace(editSql, "{ip}", ip)
    editSql = Replace(editSql, "{filename}", filename)
    con.Execute(editSql)
    con.Close
%>