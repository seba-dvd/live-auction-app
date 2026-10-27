package ro.unitbv.liveauction.gateway.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.reactive.EnableWebFluxSecurity;
import org.springframework.security.config.web.server.ServerHttpSecurity;
import org.springframework.security.web.server.SecurityWebFilterChain;

/**
 * Skeleton: everything is permitted so the stack runs end-to-end from day one.
 * <p>
 * TODO(D) S1, see docs/team/D.md:
 * <ul>
 *   <li>validate JWTs with {@code oauth2ResourceServer(...)} and an HS256 {@code ReactiveJwtDecoder} built from
 *       {@code app.jwt.secret};</li>
 *   <li>permit only the public routes of docs/api-contracts.md, require authentication for the rest of {@code /api/**};</li>
 *   <li>answer 401/403 with RFC 9457 ProblemDetail JSON;</li>
 *   <li>in a global filter: strip client-sent {@code X-User-Id}, {@code X-User-Name}, {@code X-Internal-Key},
 *       then add {@code X-User-Id} / {@code X-User-Name} from the validated token.</li>
 * </ul>
 */
@Configuration
@EnableWebFluxSecurity
public class SecurityConfig {

    @Bean
    SecurityWebFilterChain securityWebFilterChain(ServerHttpSecurity http) {
        return http
                .csrf(ServerHttpSecurity.CsrfSpec::disable)
                .httpBasic(ServerHttpSecurity.HttpBasicSpec::disable)
                .formLogin(ServerHttpSecurity.FormLoginSpec::disable)
                .cors(Customizer.withDefaults())
                .authorizeExchange(exchanges -> exchanges.anyExchange().permitAll())
                .build();
    }
}
