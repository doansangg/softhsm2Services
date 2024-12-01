import PyKCS11
import binascii
import os
from config import settings
import base64


def gen_key_softhsm2(token_label, pin, signatureAlgorithm="RSA", expirationTime=None, key_label="MyKey", key_length=2048):
    """
    Tạo một cặp khóa RSA trong SoftHSM2 với các tham số mở rộng.

    Args:
        token_label (str): Nhãn token trong SoftHSM2.
        pin (str): Mã PIN để truy cập vào token.
        accessToken (str): Access token để xác thực yêu cầu.
        signatureAlgorithm (str): Thuật toán chữ ký (mặc định: RSA).
        expirationTime (long): Thời gian hết hạn của khóa (UNIX timestamp).
        key_label (str): Nhãn cho cặp khóa.
        key_length (int): Độ dài khóa (mặc định: 2048).

    Returns:
        dict: Thông tin về cặp khóa (handle của public và private key, metadata).
    """
    try:
        # Kiểm tra thuật toán hỗ trợ
        if signatureAlgorithm != "RSA":
            raise ValueError(f"Thuật toán '{signatureAlgorithm}' không được hỗ trợ.")
        # Tải thư viện PKCS#11
        pkcs11 = PyKCS11.PyKCS11Lib()
        pkcs11.load(settings.LIB_SOFTHSM2)  # Đường dẫn tới thư viện SoftHSM2

        # Lấy danh sách slot
        slots = pkcs11.getSlotList(tokenPresent=True)
        if not slots:
            raise Exception("Không tìm thấy token nào trong SoftHSM2.")

        # Tìm slot chứa token có nhãn phù hợp
        slot = None
        for s in slots:
            token_info = pkcs11.getTokenInfo(s)
            if token_info.label.strip() == token_label:
                slot = s
                break

        if slot is None:
            raise Exception(f"Không tìm thấy token với nhãn '{token_label}'.")

        # Mở session và đăng nhập
        session = pkcs11.openSession(slot, PyKCS11.CKF_RW_SESSION)
        session.login(pin)
        key_id = os.urandom(8)
        key_id_base64 = base64.b64encode(key_id).decode('utf-8')
        #print(key_id)
        # Tạo cặp khóa RSA
        pub_template = [
            (PyKCS11.CKA_LABEL, key_label),
            (PyKCS11.CKA_CLASS, PyKCS11.CKO_PUBLIC_KEY),
            (PyKCS11.CKA_KEY_TYPE, PyKCS11.CKK_RSA),
            (PyKCS11.CKA_TOKEN, True),
            (PyKCS11.CKA_ENCRYPT, True),
            (PyKCS11.CKA_MODULUS_BITS, key_length),
            (PyKCS11.CKA_PUBLIC_EXPONENT, (1, 0, 1)),
            (PyKCS11.CKA_ID,key_id),
        ]
        
        priv_template = [
            (PyKCS11.CKA_LABEL, key_label),
            (PyKCS11.CKA_CLASS, PyKCS11.CKO_PRIVATE_KEY),
            (PyKCS11.CKA_KEY_TYPE, PyKCS11.CKK_RSA),
            (PyKCS11.CKA_TOKEN, True),
            (PyKCS11.CKA_PRIVATE, True),
            (PyKCS11.CKA_DECRYPT, True),
            (PyKCS11.CKA_ID,key_id),
        ]
        
        public_key, private_key = session.generateKeyPair(pub_template, priv_template) 
        # Đăng xuất và đóng session
        session.logout()
        session.closeSession()
        return {
            # "public_key_handle": public_key,
            # "private_key_handle": private_key,
            "kid": key_id_base64,
            "signatureAlgorithm": signatureAlgorithm,
            "expirationTime": expirationTime,
        }
    except Exception as e:
        print(f"Lỗi: {e}")
        return None


def signature_softhsm2(token_label, pin, signatureAlgorithm="CKM_SHA256_RSA_PKCS", keyID = None, key_label="MyKey", signingInput="signingInput"):
    # Tải thư viện PKCS#11
    pkcs11 = PyKCS11.PyKCS11Lib()
    pkcs11.load(settings.LIB_SOFTHSM2)

    # Lấy danh sách slot
    slots = pkcs11.getSlotList(tokenPresent=True)
    if not slots:
        raise Exception("Không tìm thấy token nào trong SoftHSM2.")

    # Tìm slot chứa token có nhãn phù hợp
    slot = None
    for s in slots:
        token_info = pkcs11.getTokenInfo(s)
        if token_info.label.strip() == token_label:
            slot = s
            break

    if slot is None:
        raise Exception(f"Không tìm thấy token với nhãn '{token_label}'.")

        # Mở session và đăng nhập
    session = pkcs11.openSession(slot, PyKCS11.CKF_RW_SESSION)
    session.login(pin)

    try:
        # Lấy private key bằng alias (CKA_LABEL)
                # Duyệt qua tất cả các đối tượng PRIVATE_KEY
        private_key = None
        for obj in session.findObjects([
            (PyKCS11.CKA_CLASS, PyKCS11.CKO_PRIVATE_KEY),
            (PyKCS11.CKA_LABEL, key_label),
            (PyKCS11.CKA_ID, base64.b64decode(keyID))
        ]):
            private_key = obj
            break

        if not private_key:
            raise RuntimeError(f"Không tìm thấy khóa bí mật với alias '{key_label}'")

        # Ánh xạ thuật toán ký số
        algorithms = {
            "CKM_SHA256_RSA_PKCS": PyKCS11.CKM_SHA256_RSA_PKCS,
            "CKM_RSA_PKCS": PyKCS11.CKM_RSA_PKCS,
            "CKM_SHA1_RSA_PKCS": PyKCS11.CKM_SHA1_RSA_PKCS,
        }
        mechanism = algorithms.get(signatureAlgorithm)
        if not mechanism:
            raise ValueError(f"Thuật toán '{signatureAlgorithm}' không được hỗ trợ")

        # Ký dữ liệu
        signature = session.sign(private_key, signingInput.encode(), PyKCS11.Mechanism(mechanism))
        signature_base64 = base64.b64encode(bytearray(signature)).decode('utf-8')
        #print("signing: ",binascii.hexlify(bytearray(signature)).decode())
        #return binascii.hexlify(bytearray(signature)).decode()
        return {"signing":signature_base64}

    finally:
        # Đóng session
        session.logout()
        session.closeSession()

def verify_signature_softhsm2(token_label, pin, signatureAlgorithm="CKM_SHA256_RSA_PKCS", keyID=None, key_label="MyKey", signingInput="signingInput", signature_base64=""):
    # Tải thư viện PKCS#11
    pkcs11 = PyKCS11.PyKCS11Lib()
    pkcs11.load(settings.LIB_SOFTHSM2)

    # Lấy danh sách slot
    slots = pkcs11.getSlotList(tokenPresent=True)
    if not slots:
        raise Exception("Không tìm thấy token nào trong SoftHSM2.")

    # Tìm slot chứa token có nhãn phù hợp
    slot = None
    for s in slots:
        token_info = pkcs11.getTokenInfo(s)
        if token_info.label.strip() == token_label:
            slot = s
            break

    if slot is None:
        raise Exception(f"Không tìm thấy token với nhãn '{token_label}'.")

    # Mở session và đăng nhập
    session = pkcs11.openSession(slot, PyKCS11.CKF_RW_SESSION)
    session.login(pin)

    try:
        # Lấy public key bằng alias (CKA_LABEL)
        public_key = None
        for obj in session.findObjects([
            (PyKCS11.CKA_CLASS, PyKCS11.CKO_PUBLIC_KEY),
            (PyKCS11.CKA_LABEL, key_label),
            (PyKCS11.CKA_ID, base64.b64decode(keyID))
        ]):
            public_key = obj
            break

        if not public_key:
            raise RuntimeError(f"Không tìm thấy khóa công khai với alias '{key_label}'")

        # Ánh xạ thuật toán xác minh chữ ký
        algorithms = {
            "CKM_SHA256_RSA_PKCS": PyKCS11.CKM_SHA256_RSA_PKCS,
            "CKM_RSA_PKCS": PyKCS11.CKM_RSA_PKCS,
            "CKM_SHA1_RSA_PKCS": PyKCS11.CKM_SHA1_RSA_PKCS,
        }
        mechanism = algorithms.get(signatureAlgorithm)
        if not mechanism:
            raise ValueError(f"Thuật toán '{signatureAlgorithm}' không được hỗ trợ")

        # Chuyển đổi signature từ base64 về byte
        signature = base64.b64decode(signature_base64)

        # Xác minh chữ ký
        is_verified = session.verify(public_key, signingInput.encode(), signature, PyKCS11.Mechanism(mechanism))

        if is_verified:
            return {"verification": "Signature is valid"}
        else:
            return {"verification": "Signature is invalid"}

    finally:
        # Đóng session
        session.logout()
        session.closeSession()