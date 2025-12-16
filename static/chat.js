var socket = io();

/* Temel DOM elementleri */
const msgBox = document.getElementById("messages");
const sendBtn = document.getElementById("sendBtn");
const msgInput = document.getElementById("msgInput");
const cipherSelect = document.getElementById("cipher");
const keyInput = document.getElementById("keyInput");

/* Secure mod elementleri */
const secureBtn = document.getElementById("secureSendBtn");
const secureAlgo = document.getElementById("secureAlgo");

let RSA_PUBLIC_KEY = null;

/* Mesaj yazdırma */
function writeMessage(text) {
    msgBox.innerHTML += `<div>${text}</div>`;
    msgBox.scrollTop = msgBox.scrollHeight;
}

/* Socket bağlantısı */
socket.on("connect", () => {
    writeMessage("Sunucuya bağlanıldı.");
    socket.emit("rsa_key_request");
});

/* Sunucu mesajları */
socket.on("server_message", (data) => {
    writeMessage("SERVER -> " + data.msg);
});

/* Klasik cipher yayınları */
socket.on("broadcast", (data) => {
    writeMessage(
        `(${data.cipher}) Orijinal: ${data.original} -> Şifreli: ${data.processed}`
    );
});

/* RSA public key al */
socket.on("rsa_public_key", (key) => {
    RSA_PUBLIC_KEY = key;
    writeMessage("RSA public key alındı.");
});

/* Secure mesaj cevabı */
socket.on("secure_response", (data) => {
    writeMessage("SERVER -> Çözülmüş Mesaj: " + data.decrypted);
});

/* Klasik chat gönderimi */
if (sendBtn) {
    sendBtn.onclick = () => {
        let msg = msgInput.value;
        if (msg.trim() === "") return;

        socket.emit("client_message", {
            message: msg,
            cipher: cipherSelect.value,
            key: keyInput.value
        });

        msgInput.value = "";
    };
}

/* Secure (AES / DES / Manuel) gönderim */
if (secureBtn) {
    secureBtn.onclick = () => {

        if (!RSA_PUBLIC_KEY) {
            writeMessage("RSA anahtarı alınamadı.");
            return;
        }

        let msg = msgInput.value;
        if (msg.trim() === "") return;

        let algorithm = secureAlgo.value;

        let symKey = algorithm.includes("DES")
            ? "8bytekey"
            : "thisis16bytekey";

        socket.emit("secure_message", {
            algorithm: algorithm,
            encrypted_key: symKey,
            message: msg
        });

        writeMessage(`SECURE (${algorithm}) -> ${msg}`);
        msgInput.value = "";
    };
}
