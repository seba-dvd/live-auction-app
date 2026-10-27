package ro.unitbv.liveauction.user.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

/**
 * user-service does NOT authenticate HTTP requests itself: the api-gateway validates the JWT and forwards
 * {@code X-User-Id} / {@code X-User-Name}. Spring Security is used here for BCrypt and (later) the JWT encoder.
 * <p>
 * TODO(D) S1: add a {@code JwtEncoder} bean (Nimbus, HS256, secret {@code app.jwt.secret}) for issuing tokens.
 * TODO(D) S2: protect {@code /internal/**} with a filter that checks {@code X-Internal-Key} against
 * {@code app.internal-api-key} (401 ProblemDetail otherwise).
 */
@Configuration
public class SecurityConfig {

    @Bean
    SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
                .csrf(AbstractHttpConfigurer::disable)
                .httpBasic(AbstractHttpConfigurer::disable)
                .formLogin(AbstractHttpConfigurer::disable)
                .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .authorizeHttpRequests(auth -> auth.anyRequest().permitAll())
                .build();
    }

    @Bean
    PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
