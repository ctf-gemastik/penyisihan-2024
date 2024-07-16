<?php

namespace app\models;

use Yii;
use yii\base\Model;

/**
 * ContactForm is the model behind the contact form.
 */
class ContactForm extends Model
{
    public $name;
    public $email;
    public $subject;
    public $body;
    public $verifyCode;


    /**
     * @return array the validation rules.
     */
    public function rules()
    {
        return [
            // name, email, subject and body are required
            [['name', 'email', 'subject', 'body'], 'required'],
            // email has to be a valid email address
            ['email', 'email'],
        ];
    }

    /**
     * @return array customized attribute labels
     */
    public function attributeLabels()
    {
        return [
            'verifyCode' => 'Verification Code',
        ];
    }

    public function setAttributes($values, $safeOnly = true)
    {
        if (is_array($values)) {
            foreach ($values as $name => $value) {
                $this->$name = $value;
            }
        }
    }

    /**
     * Sends an email to the specified email address using the information collected by this model.
     * @param string $email the target email address
     * @return bool whether the model passes validation
     */
    public function contact($email)
    {
        if ($this->validate()) {
            // Yii::$app->mailer->compose()
            //     ->setTo($email)
            //     ->setFrom([Yii::$app->params['senderEmail'] => Yii::$app->params['senderName']])
            //     ->setReplyTo([$this->email => $this->name])
            //     ->setSubject($this->subject)
            //     ->setTextBody($this->body)
            //     ->send();

            return true;
        }
        return false;
    }
}
