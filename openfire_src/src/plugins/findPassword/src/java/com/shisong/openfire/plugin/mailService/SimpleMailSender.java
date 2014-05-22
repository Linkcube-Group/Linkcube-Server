package com.shisong.openfire.plugin.mailService;

import java.util.Date;
import java.util.Properties;
import javax.mail.Address;
import javax.mail.BodyPart;
import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.Multipart;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeBodyPart;
import javax.mail.internet.MimeMessage;
import javax.mail.internet.MimeMultipart;

public class SimpleMailSender {

	public boolean sendTextMail(MailSenderInfo mailInfo) {

		MailAuthenticator authenticator = null;		// 判断是否需要身份认证
		Properties pro = mailInfo.getProperties();
		if (mailInfo.isValidate()) {			   // 如果需要身份认证，则创建一个密码验证器
			authenticator = new MailAuthenticator(mailInfo.getUserName(),mailInfo.getPassword());
		}
		// 根据邮件会话属性和密码验证器构造一个发送邮件的session
		Session sendMailSession = Session.getDefaultInstance(pro, authenticator);
		try {
			Message mailMessage = new MimeMessage(sendMailSession);        // 根据session创建一个邮件消息
			Address from = new InternetAddress(mailInfo.getFromAddress()); // 创建邮件发送者地址
			mailMessage.setFrom(from);                                     // 设置邮件消息的发送者
			Address to = new InternetAddress(mailInfo.getToAddress());     // 创建邮件的接收者地址，并设置到邮件消息中
			mailMessage.setRecipient(Message.RecipientType.TO, to);        // 设置邮件消息的主题
			mailMessage.setSubject(mailInfo.getSubject());
			mailMessage.setSentDate(new Date());          // 设置邮件消息发送的时间
			String mailContent = mailInfo.getContent();   // 设置邮件消息的主要内容
			mailMessage.setText(mailContent);
			Transport.send(mailMessage);                  // 发送邮件
			return true;
		} catch (MessagingException ex) {
			ex.printStackTrace();
		}
		return false;
	}

	public static boolean sendHtmlMail(MailSenderInfo mailInfo) {
		
		MailAuthenticator authenticator = null; // 判断是否需要身份认证
		Properties pro = mailInfo.getProperties();
		if (mailInfo.isValidate()) {            // 如果需要身份认证，则创建一个密码验证器
			authenticator = new MailAuthenticator(mailInfo.getUserName(), mailInfo.getPassword());
		}
		
		Session sendMailSession = Session.getDefaultInstance(pro, authenticator);// 根据邮件会话属性和密码验证器构造一个发送邮件的session
		try {
			Message mailMessage = new MimeMessage(sendMailSession);              // 根据session创建一个邮件消息
			Address from = new InternetAddress(mailInfo.getFromAddress());       // 创建邮件发送者地址
			mailMessage.setFrom(from);                                           // 设置邮件消息的发送者
			Address to = new InternetAddress(mailInfo.getToAddress());           // 创建邮件的接收者地址，并设置到邮件消息中
			mailMessage.setRecipient(Message.RecipientType.TO, to);              // Message.RecipientType.TO属性表示接收者的类型为TO
			mailMessage.setSubject(mailInfo.getSubject());                       // 设置邮件消息的主题
			mailMessage.setSentDate(new Date());                                 // 设置邮件消息发送的时间
			Multipart mainPart = new MimeMultipart();                            // MiniMultipart类是一个容器类，包含MimeBodyPart类型的对象
			BodyPart html = new MimeBodyPart();                                  // 创建一个包含HTML内容的MimeBodyPart
			html.setContent(mailInfo.getContent(), "text/html; charset=UTF-8");    // 设置HTML内容
			mainPart.addBodyPart(html);
			mailMessage.setContent(mainPart);                                    // 将MiniMultipart对象设置为邮件内容
			Transport.send(mailMessage);                                         // 发送邮件
			return true;
		} catch (MessagingException ex) {
			ex.printStackTrace();
		}
		return false;
	}
}