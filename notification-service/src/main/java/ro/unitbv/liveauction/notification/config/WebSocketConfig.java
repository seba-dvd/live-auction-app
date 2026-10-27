package ro.unitbv.liveauction.notification.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker;
import org.springframework.web.socket.config.annotation.StompEndpointRegistry;
import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer;

/**
 * STOMP over plain WebSocket (no SockJS). Browsers connect to {@code ws://<host>/ws}: nginx or Vite proxy it to the
 * api-gateway, which proxies it here.
 * <ul>
 *   <li>public topic: {@code /topic/auctions/{auctionId}}</li>
 *   <li>private queue: {@code /user/queue/notifications} (needs a JWT on CONNECT)</li>
 * </ul>
 * TODO(R) S2: override {@code configureClientInboundChannel(ChannelRegistration)} and register a
 * {@code ChannelInterceptor} that validates {@code Authorization: Bearer <jwt>} on CONNECT (HS256,
 * {@code app.jwt.secret}) and sets the Principal name to the userId, so that
 * {@code convertAndSendToUser(userId, "/queue/notifications", event)} reaches the right browser.
 * Anonymous connections may subscribe only to {@code /topic/auctions/**}.
 */
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    private final String[] allowedOriginPatterns;

    public WebSocketConfig(@Value("${app.websocket.allowed-origin-patterns}") String[] allowedOriginPatterns) {
        this.allowedOriginPatterns = allowedOriginPatterns;
    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws").setAllowedOriginPatterns(allowedOriginPatterns);
    }

    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        registry.enableSimpleBroker("/topic", "/queue");
        registry.setApplicationDestinationPrefixes("/app");
        registry.setUserDestinationPrefix("/user");
    }
}
