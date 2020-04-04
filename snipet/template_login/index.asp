<%@ Language=VBScript %>
<!-- #include file=conn/dbcon.inc -->

<%
    <!-- simple authorized -->
    Function Authentication(usrid, pw)
        <!-- get the auth db. -->
        set con = Server.CreateObject("ADODB.Connection")
        con.Open Connect_db()
        set fso = Server.CreateObject("Scripting.FileSystemObject")
        editSql = fso.OpenTextFile(Server.MapPath("sql/Auth.sql"), 1, False).ReadAll()
        editSql = Replace(editSql, "{USRID}", usrid)
        editSql = Replace(editSql, "{PW}", pw)
        set rs = Server.CreateObject("ADODB.Recordset")
        rs.Open editSql, con, adOpenStatic
        If Not rs.EOF Then
            <!-- is authorized (cookie is limited on 30 minite.) -->
            Authentication = true
            Response.Cookies("hbcportallogin") = usrid
            Response.Cookies("hbcportallogin").Expires = DateAdd("s", 1800, Now)
        End If
        rs.Close
        con.Close
    End Function

    <!-- check auth and cookie then if you are not login, redirect login display. -->
    usrid = Request.Form("usrid")
    pw = Request.Form("pw")
    If not Authentication(usrid, pw) Then
        buf = Request.Cookies("hbcportallogin")
        If buf <> "" Then
            usrid = buf
        Else
            Response.Redirect "login.html"
        End If
    End If

    <!-- sql_insert: access counter -->
    set con = Server.CreateObject("ADODB.Connection")
    con.Open Connect_db_IR()
    ip = Request.ServerVariables("REMOTE_ADDR")
    editSql = "INSERT INTO hbcpotal_count (access_ip, category, note, created_at) VALUES ('{ip}', 'access', 'index.asp', GETDATE())"
    editSql = Replace(editSql, "{ip}", ip)
    con.Execute(editSql)

    <!-- sql_view: access counter -->
    editSql = "SELECT FORMAT([created_at],'M/d HH') created_at, COUNT(access_ip) CNT FROM hbcpotal_count WHERE category = 'access' GROUP BY FORMAT([created_at],'M/d HH') ORDER BY created_at"
    set rs = Server.CreateObject("ADODB.Recordset")
    rs.Open editSql, con, adOpenStatic
    If Not rs.EOF Then
        Do Until rs.EOF
            If csv_access_cnt <> "" Then
                csv_access_cnt = csv_access_cnt & "\n"
            End If
            csv_access_cnt = csv_access_cnt & rs("created_at").value & "," & rs("CNT").value
            rs.MoveNext
        Loop
    End If
    rs.Close

    <!-- sql_view: click counter -->
    editSql = "SELECT note, COUNT(access_ip) CNT FROM hbcpotal_count WHERE category = 'linkclick' GROUP BY note ORDER BY CNT DESC"
    set rs = Server.CreateObject("ADODB.Recordset")
    rs.Open editSql, con, adOpenStatic
    If Not rs.EOF Then
        sql_click_cnt = "<tr><th>ファイル名</th><th>ダウンロード数</th></tr>"
        Do Until rs.EOF
            sql_click_cnt = sql_click_cnt & "<tr>"
            sql_click_cnt = sql_click_cnt & "<td>" & rs("note").value & "</td>"
            sql_click_cnt = sql_click_cnt & "<td>" & rs("CNT").value & "</td>"
            sql_click_cnt = sql_click_cnt & "</tr>"
            rs.MoveNext
        Loop
    End If
    rs.Close
    con.Close
%>

<%
    <!-- filelistの select button を押すと表示が変わる -->
    qry_mode = Request.QueryString("mode")
    If qry_mode = "" Then
        qry_mode = "model"
    End If
%>

<!DOCTYPE html>
<html>
<head>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>メインページ</title>
    
    <!-- css -->
    <link href="css/reset.css" rel="stylesheet" type="text/css">
    <link href="css/index.css" rel="stylesheet" type="text/css">

    <!-- font -->
    <link href="https://fonts.googleapis.com/css?family=Sawarabi+Gothic" rel="stylesheet">

    <!-- fontawesome -->
    <link href="https://use.fontawesome.com/releases/v5.6.1/css/all.css" rel="stylesheet">

    <!-- chart.js -->
    <script src="http://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.3.0/Chart.min.js"></script>
    <script src="js/barChart.js"></script>

    <!-- jQuery -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

    <!-- fabicon -->
    <link rel="shortcut icon" href="./favicon.ico">

</head>
<body>

    <!-- navi -->
    <div class="nav fixed">
        <ul>
            <li class="usrid"><span><b><u><% =usrid %></u></b></span></li>
            <li class="pptx"><a href="manual/Outline.pptx">概要</a></li>
            <li class="xlsx"><a href="manual/Manual.xls">マニュアル</a></li>
            <li class="logout"><a href="login.html">ログアウト</a></li>
        </ul>
    </div>
    <div class="nav decoy"></div>

    <!-- access counter -->
    <h2>アクセスカウント</h2>
    <div class="graph">
        <canvas id="barChart1" class="canvas" width="300px" height="300px"></canvas>
    </div>
    <h2>ファイルダウンロードランキング</h2>
    <div class="filelist">
        <table>
            <% =sql_click_cnt %>
        </table>
    </div>

    <!-- filelist(select button) -->
    <h2>Data (<% =qry_mode %>)</h2>
    <div class="filelist btn">
        <ul>
            <li><a href="index.asp?mode=model">機種別</a></li>
            <li><a href="index.asp?mode=mk">MK別</a></li>
            <li><a href="index.asp?mode=bk">過去分</a></li>
        </ul>
    </div>
    <!-- filelist(data table) -->
    <table class="filelist">
        <thead>
            <tr><th class="name">ファイル名</th><th>更新日時</th><th>サイズ</th></tr>
        </thead>
        <tbody>
            <%
            Set objFS = Server.CreateObject("Scripting.FileSystemObject")
            folder = "output/" & qry_mode & "/"
            buf = Server.MapPath(folder)
            Set objDIR = objFS.GetFolder(buf)
            For Each f In objDIR.Files
                fname = f.name
                size_kb = FormatNumber( f.Size / 1000, 0, 0, 0, -1)
                Response.Write "<tr>"
                Response.Write "<td class='name'><a class='link' href='" & folder & fname & "'>" & fname & "</a></td>"
                Response.Write "<td>" & f.DateLastModified & "</td>"
                Response.Write "<td class='num'>" & size_kb & "KB</td>"
                Response.Write "</tr>"
            Next
            %>
        </tbody>
    </table>

    <script type="text/javascript">
        // click counter(Ajax)
        $(".link").click(function(){
            $.post({
                  url: "clickcounter.asp"
                , data: {"filename": document.activeElement.textContent}
            })
        });
        // chart.js
        drawBarChart("barChart1", "<% =csv_access_cnt %>")
    </script>

</body>
</html>