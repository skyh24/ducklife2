function getRandomString(length) {
    var chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var lengthOfChars = chars.length;
    var result = '';
    for (var i = 0; i < len; i++) {
        result += chars[Math.floor(Math.random() * lengthOfChars)];
    }
    return result;
}