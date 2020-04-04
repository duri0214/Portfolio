<!DOCTYPE html>
<%@ Language=VBScript %>
<!-- #include file=conn/dbcon.inc -->

<%
    <!-- httpRequest.Form の確認(POSTメソッドのみ。GetはQueryStringから) -->
    Dim user_info(3)
    USER = Request.Form("worker")
    PW = Request.Form("pw")

    <!-- form が 値を '持っていた' 場合 -->
    If USER <> "" AND PW <> "" Then

        <!-- dbから属性を取得する -->
        set con = Server.CreateObject("ADODB.Connection")
        con.Open Connect_db()
        set fso = Server.CreateObject("Scripting.FileSystemObject")
        editSql = fso.OpenTextFile(Server.MapPath("sql/Auth.sql"), 1, False).ReadAll()
        set rs = Server.CreateObject("ADODB.Recordset")
        rs.Open editSql, con, adOpenStatic

        <!-- サーバーにユーザー登録情報が？ -->
        If Not rs.EOF Then
            <!-- ありました -->
            user_info(0) = rs("USER_ID").value
            user_info(1) = rs("NAME").value
            user_info(2) = rs("FACTORY_ID").value
            user_info(3) = rs("FACTORY_NAME").value
            rs.Close
            con.Close
        Else
            <!-- ありませんでした -->
            rs.Close
            con.Close
            %>
            <script type="text/javascript">
                alert("ユーザIDまたはパスワードが間違っています。");
            </script>
            <%
        End If
    Else
        Session.Contents.Remove("U_ID")
        Session.Contents.Remove("U_NAME")
        Session.Contents.Remove("U_FACTORY")
        %>
        <script type="text/javascript">
            alert("Session情報は初期化されました。");
        </script>
        <%
    End IF

    <!-- dbから属性を取得する -->
    set con = Server.CreateObject("ADODB.Connection")
    con.Open Connect_db_IR()
    set fso = Server.CreateObject("Scripting.FileSystemObject")
    editSql = fso.OpenTextFile(Server.MapPath("sql/KP_verify.sql"), 1, False).ReadAll()
    set rs = Server.CreateObject("ADODB.Recordset")
    rs.Open editSql, con, adOpenStatic

    If Not rs.EOF Then
        Do Until rs.EOF

            <!-- data -->
            sql_rs_temp = sql_rs_temp & "<tr>"
            sql_rs_temp = sql_rs_temp & "<td>" & rs("YMD").value & "</td>"
            sql_rs_temp = sql_rs_temp & "<td>" & rs("AGG").value & "</td>"
            sql_rs_temp = sql_rs_temp & "<td>" & rs("MODEL").value & "</td>"
            sql_rs_temp = sql_rs_temp & "<td>" & rs("SHOPNAME").value & "</td>"
            sql_rs_temp = sql_rs_temp & Replace("<td class={DBLQUOTE}db num{DBLQUOTE}>", "{DBLQUOTE}", chr(34)) & FormatNumber(rs("CNT").value, 0, 0, 0, -1) & "</td>"
            sql_rs_temp = sql_rs_temp & "</tr>"

            <!-- pie chart -->
            Select Case rs("AGG").value
                Case "A_BS"
                    If rs("SHOPNAME").value = "-" Then
                        If all_bs <> "" Then
                            all_bs = all_bs & "\n"
                        End If
                        all_bs = all_bs & rs("MODEL").value & "," & rs("CNT").value
                    Else
                        If koike_bs <> "" Then
                            koike_bs = koike_bs & "\n"
                        End If
                        koike_bs = koike_bs & rs("MODEL").value & "," & rs("CNT").value
                    End If
                Case "B_ON"
                    If rs("SHOPNAME").value = "-" Then
                        If all_on <> "" Then
                            all_on = all_on & "\n"
                        End If
                        all_on = all_on & rs("MODEL").value & "," & rs("CNT").value
                    Else
                        If koike_on <> "" Then
                            koike_on = koike_on & "\n"
                        End If
                        koike_on = koike_on & rs("MODEL").value & "," & rs("CNT").value
                    End If
                Case "C_MNDBS"
                    If rs("SHOPNAME").value = "-" Then
                        If all_mndbs <> "" Then
                            all_mndbs = all_mndbs & "\n"
                        End If
                        all_mndbs = all_mndbs & rs("MODEL").value & "," & rs("CNT").value
                    Else
                        If koike_mndbs <> "" Then
                            koike_mndbs = koike_mndbs & "\n"
                        End If
                        koike_mndbs = koike_mndbs & rs("MODEL").value & "," & rs("CNT").value
                    End If
            End Select

            rs.MoveNext

        Loop
    End If

    rs.Close
    con.Close
%>

<html lang="ja">
<head>
    <meta http-equiv="Content-Type" content="text/html;CHARSET=shift_jis">
    <title>HTMLの書き方</title>

    <script language="javascript">

        // chart.js
        function drawPieChart(chart_id, disp_name, data, color){
            // CSV状のデータを改行を区切りに1次元配列に割る
            var csvData = [];
            var lines = data.split("\n");
            var colors = color.split(",");
            for (var i = 0; i<lines.length; ++i){
                var cells = lines[i].split(",");
                csvData.push(cells);
            }
            // ラベル用とデータ用の配列に割る
            var tmpLabels = [];
            var tmpData = [];
            for (var row in csvData){
                tmpLabels.push(csvData[row][0]);
                tmpData.push(csvData[row][1]);
            }
            var ctx = document.getElementById(chart_id).getContext("2d");
            var cht = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: tmpLabels,
                    datasets: [{
                        backgroundColor: colors,
                        data: tmpData
                    }]
                },
                options: {
                    responsive: false,
                    rotation: 45/180*Math.PI,
                    title: {
                        display: true,
                        text: disp_name
                    }
                }
            });
        }

    </script>

    <!-- CSS -->
    <link href="css/reset.css" rel="stylesheet" type="text/css">
    <link href="css/style.css" rel="stylesheet" type="text/css">

    <!-- Font -->
    <link href="https://fonts.googleapis.com/css?family=Sawarabi+Gothic" rel="stylesheet">

    <!-- Fontawesome -->
    <link href="https://use.fontawesome.com/releases/v5.6.1/css/all.css" rel="stylesheet">

    <!-- chart.js -->
    <script src="http://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.3.0/Chart.min.js"></script>

</head>

<body>

    <!-- navi -->
    <div class="nav2">
        <ul>
            <li><a href="#R">R</a></li>
            <li><a href="#V">V</a></li>
        </ul>
    </div>
    <div class="nav">
        <ul>
            <li><a class="active" href="index.asp?mode=regist">登録</a></li>
            <li><a href="index.asp?mode=view">照会</a></li>
        </ul>
    </div>

    <!-- table data -->
    <h2>--活動サマリ</h2>
    <div class="db">
        <table>
            <tr>
                <th>YMD</th>
                <th>AGG</th>
                <th>MODEL</th>
                <th>SHOPNAME</th>
                <th>CNT</th>
            </tr>
            <% =sql_rs_temp %>
        </table>
    </div>

    <!-- chart.js -->
    <div class="graph">
        <h2>BSグラフ</h2>
        <ul>
            <li><canvas id="pieChart1" class="canvas" width="300px" height="150px"></canvas></li>
            <li><canvas id="pieChart2" class="canvas" width="300px" height="150px"></canvas></li>
        </ul>
        <h2>ONSCHEDULEグラフ</h2>
        <ul>
            <li><canvas id="pieChart3" class="canvas" width="300px" height="150px"></canvas></li>
            <li><canvas id="pieChart4" class="canvas" width="300px" height="150px"></canvas></li>
        </ul>
        <h2>MNDBSグラフ</h2>
        <ul>
            <li><canvas id="pieChart5" class="canvas" width="300px" height="150px"></canvas></li>
            <li><canvas id="pieChart6" class="canvas" width="300px" height="150px"></canvas></li>
        </ul>
    </div>

    <!-- cards -->
    <h2>本日のカード</h2>
    <div class="cards">
        <a class="card" href="#">
            <div class="card-img">
                <img src="img/icon175x175.jpg" alt="">
            </div>
            <div class="card-body">
                <time>2018.01.30</time>
                <h1 class="card-title">カード1のタイトル</h1>
                <p>カード1の説明カード1の説明カード1の説明カード1の説明カード1の説明カード1の説明</p>
            </div>
        </a>
        <a class="card" href="#">
            <div class="card-img">
                <img src="img/icon175x175.jpg" alt="">
            </div>
            <div class="card-body">
                <time>2018.01.30</time>
                <h1 class="card-title">カード2のタイトル</h1>
                <p>カード2の説明カード2の説明カード2の説明カード2の説明カード2の説明カード2の説明</p>
            </div>
        </a>
    </div>

    <h2>HTMLの書き方</h2>
    <p>はじめてのHTML</p>
    <div class="boxdesign">
        <p>
            ・どのように接続情報を取得するか<BR>
            ・Jquery（javascript）をどのように使用可能にするか<BR>
            ・CSSをどのように使用可能にするか（このテキストの赤いデザインがCSSです）<BR>
            ・フォームの処理の流れ（入力情報を送信する際の手作り関数 apply）<BR>
            ・サーバーサイド（VBScript）の処理とhtmlの変数を使った情報のやりとり<BR>
            ・SQLの発行の仕方と受け方<BR>
            など
        </p>
    </div>

    <!-- login info -->
    <h2>現在のログイン情報</h2>
    <p>
        <table>
            <tr>
                <th>USER_ID</th>
                <td><% =user_info(0) %></td>
            </tr>
            <tr>
                <th>USER_NAME</th>
                <td><% =user_info(1) %></td>
            </tr>
            <tr>
                <th>FACTORY_ID</th>
                <td><% =user_info(2) %></td>
            </tr>
            <tr>
                <th>FACTORY_NAME</th>
                <td><% =user_info(3) %></td>
            </tr>
        </table>
    </p>

    <!-- login -->
    <h2>ログインしてみましょう</h2>
    <form action="/OaM/index.asp" method="post">
        <div class="spacer10">
            <div class="label">作業者ID</div>
            <input type="text" maxlength="10" name="worker" value="<% =USER %>" placeholder="input here"/>
        </div>
        <div class="spacer10">
            <div class="label">PASSWORD</div>
            <input type="password" maxlength="15" name="pw" value="<% =PW %>" placeholder="input here"/>
        </div>
        <button class="btn-flat-border">logIn</button>
    </form>

    <!-- chart.js -->
    <script language="javascript">
        drawPieChart("pieChart1", "全体", "<% =all_bs %>", "#ccc,#ff7d6e,#ffebe9")
        drawPieChart("pieChart2", "小池製作所", "<% =koike_bs %>", "#ccc,#ff7d6e,#ffebe9")
        drawPieChart("pieChart3", "全体", "<% =all_on %>", "#ccc,#ff7d6e,#ffebe9")
        drawPieChart("pieChart4", "小池製作所", "<% =koike_on %>", "#ccc,#ff7d6e,#ffebe9")
        drawPieChart("pieChart5", "全体", "<% =all_mndbs %>", "#ccc,#ff7d6e,#ffebe9")
        drawPieChart("pieChart6", "小池製作所", "<% =koike_mndbs %>", "#ccc,#ff7d6e,#ffebe9")
    </script>

</body>

</html>