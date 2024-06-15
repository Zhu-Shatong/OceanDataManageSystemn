import rsa
import base64
# 生成密钥对并保存到文件


def generate_and_save_keys():
    (public_key, private_key) = rsa.newkeys(2048)

    # 保存公钥
    with open('public_key.pem', 'wb') as pub_file:
        pub_file.write(public_key.save_pkcs1('PEM'))

    # 保存私钥
    with open('private_key.pem', 'wb') as priv_file:
        priv_file.write(private_key.save_pkcs1('PEM'))

# 加载公钥


def load_public_key():
    with open('public_key.pem', 'rb') as pub_file:
        public_key_data = pub_file.read()
        public_key = rsa.PublicKey.load_pkcs1(public_key_data, 'PEM')
    return public_key

# 加载私钥


def load_private_key():
    with open('private_key.pem', 'rb') as priv_file:
        private_key_data = priv_file.read()
        private_key = rsa.PrivateKey.load_pkcs1(private_key_data, 'PEM')
    return private_key

# 加密函数


def encrypt_message(message: str):
    public_key = load_public_key()
    message_bytes = message.encode('utf-8')
    encrypted_message = rsa.encrypt(message_bytes, public_key)
    # 将加密的字节数据转换为Base64字符串
    encrypted_message_base64 = base64.b64encode(
        encrypted_message).decode('utf-8')
    return encrypted_message_base64

# 解密函数


def decrypt_message(encrypted_message_base64: str):
    # 将Base64字符串转换回字节数据
    private_key = load_private_key()
    encrypted_message = base64.b64decode(encrypted_message_base64)
    decrypted_message = rsa.decrypt(encrypted_message, private_key)
    return decrypted_message.decode('utf-8')

# 示例使用


def main():
    # 生成并保存密钥对
    #generate_and_save_keys()

    # 待加密的消息
    message = "1977"

    # 加密消息
    encrypted_message = encrypt_message(message)
    print(f"Encrypted Message: {encrypted_message}")

    # 解密消息
    decrypted_message = decrypt_message(encrypted_message)
    print(f"Decrypted Message: {decrypted_message}")


if __name__ == "__main__":
    main()
