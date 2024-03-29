package com.shisong.openfire.plugin.mailService;

import java.util.Properties;
/** 
 *
 * 记录发送邮件所需的各种信息，如发送邮件服务器的地址、端口号、发件人邮箱、收件人邮箱等。
 * 
 * @author Shisong
 */
public class MailSenderInfo {
	/**
	 * mailServerHost = "smtp.163.com"
	 * mailServerPort = "25"
	 * fromAddress    = "linkcube2013@163.com"
	 * userName       = "linkcube2013@163.com"
	 * password       = "shisong"
	 */
	private String mailServerHost;	        // 发送邮件的服务器的IP(或主机地址)
	private String mailServerPort = "25";	// 发送邮件的服务器的端口
	private String fromAddress;	            // 发件人邮箱地址
	private String toAddress;	            // 收件人邮箱地址
	private String userName;	            // 登陆邮件发送服务器的用户名
	private String password;	            // 登陆邮件发送服务器的密码
	private boolean validate = false;	    // 是否需要身份验证

	private String subject;	                // 邮件主题
	private String content;                 // 邮件的文本内容
	private String[] attachFileNames;	    // 邮件附件的文件名

	public Properties getProperties() {
		Properties p = new Properties();
		p.put("mail.smtp.host", this.mailServerHost);
		p.put("mail.smtp.port", this.mailServerPort);
		p.put("mail.smtp.auth", validate ? "true" : "false");
		return p;
	}

	public String getMailServerHost() {
		return mailServerHost;
	}

	public void setMailServerHost(String mailServerHost) {
		this.mailServerHost = mailServerHost;
	}

	public String getMailServerPort() {
		return mailServerPort;
	}

	public void setMailServerPort(String mailServerPort) {
		this.mailServerPort = mailServerPort;
	}

	public boolean isValidate() {
		return validate;
	}

	public void setValidate(boolean validate) {
		this.validate = validate;
	}

	public String[] getAttachFileNames() {
		return attachFileNames;
	}

	public void setAttachFileNames(String[] fileNames) {
		this.attachFileNames = fileNames;
	}

	public String getFromAddress() {
		return fromAddress;
	}

	public void setFromAddress(String fromAddress) {
		this.fromAddress = fromAddress;
	}

	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}

	public String getToAddress() {
		return toAddress;
	}

	public void setToAddress(String toAddress) {
		this.toAddress = toAddress;
	}

	public String getUserName() {
		return userName;
	}

	public void setUserName(String userName) {
		this.userName = userName;
	}

	public String getSubject() {
		return subject;
	}

	public void setSubject(String subject) {
		this.subject = subject;
	}

	public String getContent() {
		return content;
	}

	public void setContent(String textContent) {
		this.content = textContent;
	}
}