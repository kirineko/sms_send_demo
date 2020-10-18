<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up</title>
    <script src="https://cdn.bootcss.com/jquery/3.5.0/jquery.min.js"></script>
</head>
<body>
    <h2>Sign up</h2>
    <hr>
    <form action="/signup" method="post">
        手机号码:
        <input type="text" name="mobile" id="mobile">
        验证码:
        <input type="text" name="code" id="code">
        <input type="button" value="获取验证码" id="getcode">
        <input type="submit" value="注册">
    </form>
</body>
<script>
    $('#getcode').click(()=>{
        let mobile = $('#mobile').val()
        let sec = 60
        $('#getcode').attr('disabled', true)
        $('#getcode').val(`${sec}s后重新获取`)
        timer = setInterval(setcode, 1000)
        function setcode() {
            if (sec <= 0) {
                clearInterval(timer)
                $('#getcode').attr('disabled', false)
                $('#getcode').val('重新获取验证码')
            } else {
                sec--
                $('#getcode').val(`${sec}s后重新获取`)
            }
        }
        data = {
            'mobile': mobile
        }
        $.post('/getcode', data, (result)=>{
            console.log(result)
        })
    })
</script>
</html>