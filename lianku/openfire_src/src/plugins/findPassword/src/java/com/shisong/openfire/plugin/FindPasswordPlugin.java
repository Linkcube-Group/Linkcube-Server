package com.shisong.openfire.plugin;

import java.io.File;

import org.jivesoftware.openfire.XMPPServer;
import org.jivesoftware.openfire.container.Plugin;
import org.jivesoftware.openfire.container.PluginManager;

/**
 * @author Shisong
 */
public class FindPasswordPlugin implements Plugin {

	
	public FindPasswordPlugin() {
	}

	@Override
	public void initializePlugin(PluginManager manager, File pluginDirectory) {
		XMPPServer server = XMPPServer.getInstance();   
		server.getIQDiscoInfoHandler().addServerFeature(FindPasswordIQHandler.NAME_SPACE);
		server.getIQRouter().addHandler(new FindPasswordIQHandler());
	}

	@Override
	public void destroyPlugin() {
	}

}
