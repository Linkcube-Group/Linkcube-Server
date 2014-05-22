package com.shisong.openfire.plugin.mailService;

public class LinkcubeFindPassword {

	private static String mailServerHost = "smtp.163.com";
	private static String mailServerPort = "25";
	private static String fromAddress    = "linkcube2013@163.com";
	private static String userName       = "linkcube2013@163.com";
	private static String password       = "shisong";
	private static String subject        = "连酷密码找回";   //邮件标题
	
	public static void sendTo(String toAddress, String findPassword)
	{
		MailSenderInfo mailInfo = new MailSenderInfo();
		mailInfo.setMailServerHost(mailServerHost);
		mailInfo.setMailServerPort(mailServerPort);
		mailInfo.setValidate(true);
		mailInfo.setUserName(userName);
		mailInfo.setPassword(password);
		mailInfo.setFromAddress(fromAddress);
		mailInfo.setToAddress(toAddress);
		mailInfo.setSubject(subject);

		// 邮件内容
		StringBuffer buffer = new StringBuffer();
		buffer.append("该邮件为系统邮件，请勿回复。\n\n");
		buffer.append("您的连酷密码是："+ findPassword +"\n\n");
		buffer.append("找回密码后，请尽快删除该邮件，以免给您带来不必要的损失\n\n");
		mailInfo.setContent(buffer.toString());

		// 发送邮件
		SimpleMailSender sms = new SimpleMailSender();
		sms.sendTextMail(mailInfo);// 发送文体格式
		//SimpleMailSender.sendHtmlMail(mailInfo);// 发送html格式
	}
}
