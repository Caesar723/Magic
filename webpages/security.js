class Security_process{

    constructor(){
        
    }

    async encrypt(message,pem){
        const publicKey=await this.importPublicKey(pem)
        console.log(publicKey)
        const encoder = new TextEncoder();
        const encodedMessage = encoder.encode(message);
        console.log(1)
        const encryptedMessage = await window.crypto.subtle.encrypt(
            {
                name: 'RSA-OAEP',
            },
            publicKey,
            encodedMessage
        );
        console.log(2)
        return this.arrayBufferToBase64(new Uint8Array(encryptedMessage));
    }
    async importPublicKey(pem) {
        const binaryDer = window.atob(pem.split('\n').slice(1, -2).join(''));
        const array = new Uint8Array(binaryDer.length);
        for (let i = 0; i < binaryDer.length; i++) {
            array[i] = binaryDer.charCodeAt(i);
        }
        return window.crypto.subtle.importKey(
            'spki',
            array.buffer,
            {
                name: 'RSA-OAEP',
                hash: 'SHA-256',
            },
            false,
            ['encrypt']
        );
    }
    arrayBufferToBase64(buffer) {
        let binary = '';
        const bytes = new Uint8Array(buffer);
        const len = bytes.byteLength;
        for (let i = 0; i < len; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return window.btoa(binary);
    }

}