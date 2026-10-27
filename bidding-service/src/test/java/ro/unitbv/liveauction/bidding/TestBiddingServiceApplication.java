package ro.unitbv.liveauction.bidding;

import org.springframework.boot.SpringApplication;

/**
 * Runs the service against a throw-away MySQL container (no Docker Compose needed): run this class from IntelliJ.
 */
public class TestBiddingServiceApplication {

    public static void main(String[] args) {
        SpringApplication.from(BiddingServiceApplication::main).with(TestcontainersConfiguration.class).run(args);
    }
}
