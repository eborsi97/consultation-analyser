//
// For guidance on how to create routes see:
// https://prototype-kit.service.gov.uk/docs/create-routes
//

const govukPrototypeKit = require('govuk-prototype-kit')
const router = govukPrototypeKit.requests.setupRouter()

router.post('/upload-file', (request, response) => {
    if (request.session.data.file) {
        request.session.data['upload-error'] = false;
        response.redirect('/upload-success');
    } else {
        request.session.data['upload-error'] = true;
        response.redirect('/upload');
    }
});
