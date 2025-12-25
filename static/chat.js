function strToUint8(str) {
    return new TextEncoder().encode(str);
}

function uint8ToBase64(arr) {
    return btoa(String.fromCharCode(...arr));
}

var socket = io();

const msgBox = document.getElementById("messages");

/* ======================
   KLASİK CHAT
====================== */
const sendBtn = document.getElementById("sendBtn");
const msgInput = document.getElementById("msgInput");
const cipherSelect = document.getElementById("cipher");
const keyInput = document.getElementById("keyInput");

/* ======================
   SECURE CHAT
====================== */
const secureSendBtn = document.getElementById("secureSendBtn");
const secureAlgoSelect = document.getElementById("secureAlgo");
const secureMsgInput = document.getElementById("msgSecureInput");

let RSA_PUBLIC_KEY = null;

/* ======================
   YARDIMCI
====================== */
function writeMessage(text) {
    msgBox.innerHTML += `<div>${text}</div>`;
    msgBox.scrollTop = msgBox.scrollHeight;
}

/* ======================
   SOCKET EVENTS
====================== */
socket.on("connect", () => {
    writeMessage("Sunucuya bağlanıldı.");
    socket.emit("rsa_key_request");
});

socket.on("server_message", (data) => {
    writeMessage("SERVER -> " + data.msg);
});

socket.on("broadcast", (data) => {
    writeMessage(
        `(${data.cipher}) Orijinal: ${data.original} → Şifreli: ${data.processed}`
    );
});

/* RSA PUBLIC KEY */
socket.on("rsa_public_key", (key) => {
    RSA_PUBLIC_KEY = key;
    writeMessage("RSA public key alındı.");
});

/* ======================
   SECURE RESPONSE
====================== */
socket.on("secure_response", (data) => {
    writeMessage(`
        <b>SECURE CHAT</b><br>
        Algoritma: <b>${data.algo}</b><br>
        Şifreli: <code>${data.encrypted}</code><br>
        Çözülmüş: <b>${data.decrypted}</b><br>
        RSA Süre: ${data.rsa_ms} ms<br>
        Crypto Süre: ${data.crypto_ms} ms
        <hr>
    `);
});

/* ======================
   KLASİK GÖNDER
====================== */
if (sendBtn) {
    sendBtn.onclick = () => {
        let msg = msgInput.value.trim();
        if (!msg) return;

        socket.emit("client_message", {
            message: msg,
            cipher: cipherSelect.value,
            key: keyInput.value
        });

        msgInput.value = "";
    };
}

/* ======================
   SECURE GÖNDER
====================== */
if (secureSendBtn) {
    secureSendBtn.onclick = async () => {
        let msg = secureMsgInput.value.trim();
        if (!msg || !RSA_PUBLIC_KEY) return;

        let algo = secureAlgoSelect.value;

        // Simetrik anahtar
        let symKey = algo === "DES"
            ? "8bytekey"
            : "thisis16bytekey!"; // 16 byte

        // Mesajı BASE64 "şifreli" gibi gönderiyoruz
        // (gerçek AES/DES server'da yapılacak)
        let encryptedMessage = btoa(msg);

        // RSA ile anahtar şifreleme (string olarak)
        let encryptedKey = btoa(symKey);

        socket.emit("secure_message", {
            algorithm: algo,
            message: encryptedMessage,
            encrypted_key: encryptedKey
        });

        writeMessage(`SECURE (${algo}) → Şifreli mesaj gönderildi`);
        secureMsgInput.value = "";
    };
}

