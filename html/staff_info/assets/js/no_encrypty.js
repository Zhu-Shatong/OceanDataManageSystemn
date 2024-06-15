var PassPhrase = "Harsh Passwd"
var Bits = 1024
var MattsRSAkey = cryptico.generateRSAKey(PassPhrase, Bits)
var MattsPublicKeyString = cryptico.publicKeyString(MattsRSAkey)

var divide_symbol = '~'

/*
    函数说明: 对账号进行加密
    参数解释:
        input_no: 输入的账号
    返回值解释: 返回加密后的账号字符
*/ 
function generate_passwd(input_no)
{
    var EncryptionResult = cryptico.encrypt(input_no, MattsPublicKeyString)
    return EncryptionResult.cipher
}

/*
    函数说明: 对账号进行解密
    参数解释:
        input_ciphe: 输入的账号加密串
    返回值解释: 返回解密后的账号
*/ 
function generate_no(input_cipher)
{
    var DecryptionResult = cryptico.decrypt(input_cipher, MattsRSAkey);
    return DecryptionResult.plaintext
}

/*
    函数说明: 传入账号获取生成的url地址
    参数解释:
        url: 传入的url信息
        no_list: 要添加的账号列表
    返回值解释: 返回加密完成的url
*/ 
function url_generate(url, no_list)
{
    var res_url = url + '?'
    for(var i in no_list){
        res_url += divide_symbol + generate_passwd(no_list[i].toString())
    }
    return res_url
}

/*
    函数说明: 传入所需账号的个数，生成账号所对应的列表
    参数解释:
        url: 原始的url信息
    返回值解释: 返回账号的列表
*/ 
function url_parser(url)
{
    var no_encry = url.split(divide_symbol)
    var res = []
    for(var i = 1; i < no_encry.length; i++){
        res.push(parseInt(generate_no(no_encry[i])))
    }
    return res
}

