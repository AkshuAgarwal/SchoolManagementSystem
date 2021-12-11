import React from 'react';
import PropTypes from 'prop-types';
import { Form as FormComp, Button } from 'react-bootstrap';

/*
data = {
    fields: [
        {
            controlID: "...",
            name: "...",
            type: "...",
            placeholder: "...",
            text: "..." or null
        },
        {
            controlID: "...",
            name: "...",
            type: "...",
            placeholder: "...",
            text: "..." or null
        },
    ],
    extraComponents: [
        <components>
    ] or null
}

]
*/

function Form({ onSubmit, data }) {
    var fields = [];
    for (const field of data.fields) {
        fields.push(
            <FormComp.Group className="mb-3" controlId={field.controlID}>
                <FormComp.Label>{field.name}</FormComp.Label>
                <FormComp.Control type={field.type} placeholder={field.placeholder} />
                {
                    field.text ? (
                        <FormComp.Text className="text-muted">
                            {field.text}
                        </FormComp.Text>
                    ) : (null)
                }
            </FormComp.Group>
        );
    }

    return (
        <FormComp onSubmit={onSubmit}>
            {fields}
            {data.extraComponents}
            <Button varient="primary" type="submit">Submit</Button>
        </FormComp>
    );
}

Form.propTypes = {
    onSubmit : PropTypes.func.isRequired,
    data     : PropTypes.exact({
        fields: PropTypes.arrayOf(PropTypes.exact({
            controlID   : PropTypes.string.isRequired,
            name        : PropTypes.string.isRequired,
            type        : PropTypes.string.isRequired,
            placeholder : PropTypes.string.isRequired,
            text        : PropTypes.oneOfType([
                PropTypes.string.isRequired,
                PropTypes.object.isRequired
            ]).isRequired
        }).isRequired).isRequired,
        extraComponents: PropTypes.oneOfType([
            PropTypes.object.isRequired,
            PropTypes.arrayOf(PropTypes.element.isRequired)
        ]).isRequired
    }).isRequired
};

export default Form;
