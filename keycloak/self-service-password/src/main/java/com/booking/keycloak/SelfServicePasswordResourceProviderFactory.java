package com.booking.keycloak;

import jakarta.ws.rs.ForbiddenException;
import jakarta.ws.rs.NotAuthorizedException;
import org.keycloak.models.KeycloakSession;
import org.keycloak.models.KeycloakSessionFactory;
import org.keycloak.services.managers.AppAuthManager.BearerTokenAuthenticator;
import org.keycloak.services.managers.AuthenticationManager.AuthResult;
import org.keycloak.services.resource.RealmResourceProvider;
import org.keycloak.services.resource.RealmResourceProviderFactory;

public final class SelfServicePasswordResourceProviderFactory
    implements RealmResourceProviderFactory {

  public static final String ID = "self-service";
  private static final String SPA_CLIENT_ID = "events-api";

  @Override
  public RealmResourceProvider create(KeycloakSession session) {
    return new RealmResourceProvider() {
      @Override
      public Object getResource() {
        AuthResult authResult =
            new BearerTokenAuthenticator(session).authenticate();
        if (authResult == null || authResult.user() == null) {
          throw new NotAuthorizedException("Bearer");
        }
        if (authResult.client() == null
            || !SPA_CLIENT_ID.equals(authResult.client().getClientId())) {
          throw new ForbiddenException("Unsupported client");
        }

        return new SelfServicePasswordResource(
            session, authResult.user(), session.getContext().getRealm());
      }

      @Override
      public void close() {}
    };
  }

  @Override
  public void init(org.keycloak.Config.Scope config) {}

  @Override
  public void postInit(KeycloakSessionFactory factory) {}

  @Override
  public void close() {}

  @Override
  public String getId() {
    return ID;
  }
}
