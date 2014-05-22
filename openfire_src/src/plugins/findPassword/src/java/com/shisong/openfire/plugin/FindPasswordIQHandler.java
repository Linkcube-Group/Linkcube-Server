package com.shisong.openfire.plugin;

import java.util.ArrayList;
import java.util.Iterator;

import org.dom4j.Element;
import org.jivesoftware.openfire.IQHandlerInfo;
import org.jivesoftware.openfire.auth.DefaultAuthProvider;
import org.jivesoftware.openfire.auth.UnauthorizedException;
import org.jivesoftware.openfire.disco.ServerFeaturesProvider;
import org.jivesoftware.openfire.handler.IQHandler;
import org.jivesoftware.openfire.session.ClientSession;
import org.jivesoftware.openfire.user.UserNotFoundException;
import org.xmpp.packet.IQ;
import org.xmpp.packet.PacketError;

import com.shisong.openfire.plugin.mailService.LinkcubeFindPassword;

public class FindPasswordIQHandler extends IQHandler implements
		ServerFeaturesProvider {

	public static final String NAME_SPACE = "jabber:iq:findPassword";
	private static final String MODULE_NAME = "findpassword Handler Plugin";

	private IQHandlerInfo info;

	public FindPasswordIQHandler() {
		super(MODULE_NAME);
		info = new IQHandlerInfo("query", NAME_SPACE);
	}

	@Override
	public IQ handleIQ(IQ packet) throws UnauthorizedException {
		//System.out.println("request iq:" + packet.toXML());
		ClientSession session = sessionManager.getSession(packet.getFrom());
		IQ reply = null;
		if (session == null) {
			// This error packet will probably won't make it through
			reply = IQ.createResultIQ(packet);
			reply.setError(PacketError.Condition.internal_server_error);  //服务器内部错误
			return reply;
		}
		if (IQ.Type.get.equals(packet.getType())) {
			Element iqElement = packet.getChildElement();
			String email = iqElement.elementText("username");
			String username = email.replace("@", "-");
			reply = IQ.createResultIQ(packet);
			DefaultAuthProvider authProvider = new DefaultAuthProvider();
			try {
				String pwd = authProvider.getPassword(username);
				LinkcubeFindPassword.sendTo(email, pwd);   //发送邮件
			} catch (UserNotFoundException e) {
				reply.setError(PacketError.Condition.item_not_found);   //查无此用户
			}
		}
		if (reply != null) {
			// why is this done here instead of letting the iq handler do it?
			session.process(reply);
		}
		//System.out.println("reply iq:" + reply.toXML());
		return null;
	}

	@Override
	public IQHandlerInfo getInfo() {
		return info;
	}

	@Override
	public Iterator<String> getFeatures() {
		ArrayList<String> features = new ArrayList<String>();
		features.add(NAME_SPACE);
		return features.iterator();
	}

}
