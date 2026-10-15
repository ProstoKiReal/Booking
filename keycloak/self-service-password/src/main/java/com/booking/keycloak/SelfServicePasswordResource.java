package com.booking.keycloak;

import jakarta.enterprise.inject.Vetoed;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.keycloak.models.KeycloakSession;
import org.keycloak.models.ModelException;
import org.keycloak.models.RealmModel;
import org.keycloak.models.UserCredentialModel;
import org.keycloak.models.UserModel;
import org.keycloak.services.managers.BruteForceProtector;

import java.util.Set;

@Path("/")
@Vetoed
public final class SelfServicePasswordResource {

  private static final int MAX_PASSWORD_LENGTH = 256;
  private static final Set<String> PASSWORD_CATEGORY = Set.of("password");

  private final KeycloakSession session;
  private final UserModel user;
  private final RealmModel realm;

  SelfServicePasswordResource(
      KeycloakSession session, UserModel user, RealmModel realm) {
    this.session = session;
    this.user = user;
    this.realm = realm;
  }

  @POST
  @Path("password")
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  public Response changePassword(ChangePasswordRequest request) {
    if (request == null
        || isBlank(request.currentPassword)
        || isBlank(request.newPassword)
        || request.currentPassword.length() > MAX_PASSWORD_LENGTH
        || request.newPassword.length() > MAX_PASSWORD_LENGTH
        || request.currentPassword.equals(request.newPassword)) {
      return error(Response.Status.BAD_REQUEST, "Проверьте введённые данные.");
    }

    BruteForceProtector bruteForceProtector =
        session.getProvider(BruteForceProtector.class);
    if (realm.isBruteForceProtected()
        && (bruteForceProtector.isTemporarilyDisabled(session, realm, user)
            || bruteForceProtector.isPermanentlyLockedOut(session, realm, user))) {
      return error(
          Response.Status.TOO_MANY_REQUESTS,
          "Слишком много попыток. Попробуйте позже.");
    }

    if (!user
        .credentialManager()
        .isValid(UserCredentialModel.password(request.currentPassword))) {
      if (realm.isBruteForceProtected()) {
        bruteForceProtector.failedLogin(
            realm,
            user,
            session.getContext().getConnection(),
            session.getContext().getUri(),
            PASSWORD_CATEGORY);
      }
      return error(Response.Status.BAD_REQUEST, "Текущий пароль указан неверно.");
    }

    if (realm.isBruteForceProtected()) {
      bruteForceProtector.successfulLogin(
          realm,
          user,
          session.getContext().getConnection(),
          session.getContext().getUri(),
          PASSWORD_CATEGORY);
    }

    try {
      boolean updated = user
          .credentialManager()
          .updateCredential(UserCredentialModel.password(request.newPassword));
      if (!updated) {
        return error(
            Response.Status.BAD_REQUEST,
            "Пароль не соответствует политике безопасности.");
      }
    } catch (ModelException exception) {
      return error(
          Response.Status.BAD_REQUEST,
          "Пароль не соответствует политике безопасности.");
    }

    return Response.noContent().build();
  }

  private static boolean isBlank(String value) {
    return value == null || value.isBlank();
  }

  private static Response error(Response.Status status, String message) {
    return Response.status(status)
        .type(MediaType.APPLICATION_JSON)
        .entity(new ErrorResponse(message))
        .build();
  }

  public static final class ChangePasswordRequest {
    public String currentPassword;
    public String newPassword;
  }

  public record ErrorResponse(String message) {}
}
