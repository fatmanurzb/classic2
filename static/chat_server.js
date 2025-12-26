var socket = io();

const msgBox = document.getElementById("messages");
const sendBtn = document.getElementById("sendBtn");
const msgInput = document.getElementById("msgInput");
const cipherSelect = document.getElementById("cipher");
const keyInput = document.getElementById("keyInput");

function writeMessage(text) {
    msgBox.innerHTML += `<div>${text}</div>`;
    msgBox.scrollTop = msgBox.scrollHeight;
}

socket.on("connect", () => {
    writeMessage("SERVER -> Sunucuya bağlanıldı.");
});

socket.on("server_message", (data) => {
    writeMessage("SERVER -> " + data.msg);
});

/* SADECE DEŞİFRELEME SONUCU */
socket.on("server_decrypt_response", (data) => {
    writeMessage(
        ` (${data.cipher}) Şifreli: ${data.encrypted} → Çözülmüş: ${data.decrypted}`
    );
});

/* GÖNDER = DEŞİFRELE */
sendBtn.onclick = () => {
    let msg = msgInput.value.trim();
    if (!msg) return;

    socket.emit("server_decrypt_message", {
        message: msg,
        cipher: cipherSelect.value,
        key: keyInput.value
    });

    msgInput.value = "";
};
