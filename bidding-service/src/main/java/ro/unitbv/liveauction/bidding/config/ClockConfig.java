package ro.unitbv.liveauction.bidding.config;

import java.time.Clock;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * The only source of "now" in this service: inject {@link Clock} and use {@code Instant.now(clock)}.
 * Tests replace it with {@code Clock.fixed(...)} to control time.
 */
@Configuration
public class ClockConfig {

    @Bean
    Clock clock() {
        return Clock.systemUTC();
    }
}
