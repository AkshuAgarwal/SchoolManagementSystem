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

function Form({ data, onSubmit }) {
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
        )
    };

    return (
        <FormComp onSubmit={onSubmit}>
            {fields}
            {data.extraComponents}
            <Button varient="primary" type="submit">Submit</Button>
        </FormComp>
    )
}
export default Form;