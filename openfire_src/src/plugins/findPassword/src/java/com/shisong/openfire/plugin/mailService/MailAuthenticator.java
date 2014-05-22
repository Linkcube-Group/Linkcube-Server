package com.shisong.openfire.plugin.mailService;

import javax.mail.Authenticator;
import javax.mail.PasswordAuthentication;

/**
 * 
 * 邮箱用户名和密码认证器
 * 
 * @author Shisong
 */

public class MailAuthenticator extends Authenticator {
	String userName = null;
	String password = null;

	public MailAuthenticator(){
	}
	
	public MailAuthenticator(String username, String password) {
		this.userName = username;
		this.password = password;
	}

	protected PasswordAuthentication getPasswordAuthentication() {
		return new PasswordAuthentication(userName, password);
	}
}
